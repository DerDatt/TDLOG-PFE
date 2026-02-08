from django.db import models
from django import forms
from django.contrib.auth.models import User

import pandas as pd

from .convertisseur import test_key
from . import utils


from pdf_creation.generate_text import generate_pdf_file

from .widgets import CustomClearableImageInput


class WholeDocument(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # this dict contains all field-names that should have an auto translate button
        self.autotranslatable = {}
        self.fill_fields_with_csv()

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="dokument"
    )

    @staticmethod
    def strip_name_of_underscores_begin_end_between(name: str) -> str:
        # Remove underscores at the beginning and end, and inside the string
        return name.lstrip('_').rstrip('_').replace('_', ' ')

    @staticmethod
    def replace_EN_with_FR(s: str) -> str:
        return s.replace("_EN_", "_FR_")

    @staticmethod
    def replace_FR_with_EN(s: str) -> str:
        return s.replace("_FR_", "_EN_")

    def fill_fields_with_csv(self):
        path_csv = "appPFE/field_data.csv"
        df = pd.read_csv(path_csv)  # , header=None) #, usecols=[0,1,2])
        # df.columns = ['name', 'field_type']
        # df = pd.read_csv("datei.csv", header=None, usecols=[0,1,2,3])
        for _, row in df.iterrows():
            name = row["name"]
            field_type = row["field_type"]

            field = None
            if field_type == "field_type":
                continue    # skip header
            if field_type == "CharField":
                field = forms.CharField(label=self.strip_name_of_underscores_begin_end_between(name))
                # check if autotranslate button should be set: 
                possible_autotranslatable = row.iloc[2] 
                # print("possible_autotranslatable", possible_autotranslatable)
                if possible_autotranslatable == "autotranslatable":

                    self.autotranslatable[name] = self.replace_FR_with_EN(name)
                    # print("name", name)
                    # print("self.replace_FR_with_EN(name)", self.replace_FR_with_EN(name))

            elif field_type == "BooleanField":
                if "check" in name.lower():
                    required = True
                else:
                    required = False
                field = forms.BooleanField(label=self.strip_name_of_underscores_begin_end_between(name), required=required)
            elif field_type == "ImageField":
                # field = models.ImageField(label=self.strip_name_of_underscores(name), allow_empty_file=True, upload_to='images/')
                field = forms.ImageField(
                    label=self.strip_name_of_underscores_begin_end_between(name), 
                    required=False,
                    widget=CustomClearableImageInput  # Benutzerdefiniertes Widget verwenden
                )
                # __Photo_portrait__,image_field
            elif field_type == "ChoiceField":
                # values from col 3 are the possible choices
                values_from_col_3 = [
                    row[col] for col in df.columns[2:] if pd.notna(row[col])
                ]
                choices = [("", "Choisissez un élément.")]
                choices += [(value, value) for value in values_from_col_3]
                field = forms.ChoiceField(label=self.strip_name_of_underscores_begin_end_between(name), required=True, choices=choices)
            else:
                print("ERROR IN FILETYPE IN THE CSV, field_type was \"" + field_type + "\". ")
            if field:
                self.fields[name] = field

    def clean(self):
        cleaned = super().clean()    
        # when I add an error, 'cleaned' gets changed => I have to make copy beforehand
        cleaned_copy = cleaned.copy()

        for key, value in cleaned_copy.items():
            errorText = test_key(key, value)
            if errorText:
                self.add_error(key, errorText)
        
        # Validation: Check if confirmation checkbox for translated fields was checked
        # (only if the checkbox is present in the request, i.e. if it was visible)
        for en_field_name in self.autotranslatable.values():
            checkbox_name = f"translation_confirmed_{en_field_name}"
            # If the checkbox is present in the request (was visible), it must be checked
            if checkbox_name in self.data:
                if self.data[checkbox_name] != 'on':
                    self.add_error(en_field_name, "You must confirm that you have reviewed the translation.")

        return cleaned

    def send(self, user): 
        d = self.cleaned_data
        # call function in generate_text.py: 
        generate_pdf_file(d, name_for_picture=utils.name_for_picture(user))

    def add_dynamic_field(self, name, field):
        self.fields[name] = field

    def printFields(self): 
        for name, field in self.fields.items():
            print(name, field)    
