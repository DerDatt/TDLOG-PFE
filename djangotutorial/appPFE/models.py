import datetime
from sqlite3 import adapt

from django.db import models
from django.utils import timezone
from django.contrib import admin 
from django import forms

import pandas as pd

from .convertisseur import test_key


from pdf_creation.generate_text import generate_pdf_file

from db_management.Generation_PDF import create_user


from mysite.settings import MEDIA_ROOT

class WholeDocument(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fill_fields_with_csv()

    @staticmethod
    def strip_name_of_underscores(name: str) -> str:
        # Remove underscores only at the beginning and end, not inside the string
        return name.lstrip('_').rstrip('_').replace('_', ' ')

    def fill_fields_with_csv(self):

        name = self.strip_name_of_underscores("__hi__")

        path_csv = "appPFE/field_data.csv"
        df = pd.read_csv(path_csv) # , header=None) #, usecols=[0,1,2])
        # df.columns = ['name', 'field_type']
        # df = pd.read_csv("datei.csv", header=None, usecols=[0,1,2,3])
        for _, row in df.iterrows():
            name = row["name"]
            field_type = row["field_type"]

            field = None
            if field_type == "field_type":
                continue    # skip header
            if field_type == "text_field":
                field = forms.CharField(label=self.strip_name_of_underscores(name))
            elif field_type == "checkbox":
                if "check" in name.lower():
                    required = True
                else:
                    required = False
                field = forms.BooleanField(label=self.strip_name_of_underscores(name), required=required)
            elif field_type == "image_field":
                # field = models.ImageField(label=self.strip_name_of_underscores(name), allow_empty_file=True, upload_to='images/')
                field = forms.ImageField(label=self.strip_name_of_underscores(name), required=False) #, upload_to='images/')
                # __Photo_portrait__,image_field
            elif field_type == "choice_field":
                # values from col 3 are the possible choices
                values_from_col_3 = [
                    row[col] for col in df.columns[2:] if pd.notna(row[col])
                ]
                choices = [("", "Choisissez un élément.")]
                choices += [(value, value) for value in values_from_col_3]
                field = forms.ChoiceField(label=self.strip_name_of_underscores(name), required=True, choices=choices)
            else:
                print("ERROR IN FILETYPE IN THE CSV, field_type was \"" + field_type + "\". ")
            if field:
                self.fields[name] = field

    def clean(self):
        cleaned = super().clean()      


        # key = "__Promotion__"
        # val = cleaned.get(key)
        # if not val.isdigit():
        #     self.add_error(key, "Promotion must be a number. ")
        # elif int(val) > 30:
        #     self.add_error(key, "Promotion is maximal 30")
        

        # this can become for loop over keys

        # when I add an error, 'cleaned' gets changed => I have to make copy beforehand

        cleaned_copy = cleaned.copy()

        for key, value in cleaned_copy.items():
            errorText = test_key(key, value)
            if errorText:
                self.add_error(key, errorText)

        return cleaned

    def save(self): 

        d = self.cleaned_data

        # call function in generate_text.py: 
        generate_pdf_file(d)

        # print(self.cleaned_data)

    def add_dynamic_field(self, name, field):
        self.fields[name] = field
    def printFields(self): 
        for name, field in self.fields.items():
            print(name, field)    

class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fill_login_field()

    def fill_login_field(self):

        # create 'username'-field
        name="username"
        self.fields[name] = forms.CharField(label=name)

        # create 'password'-field: 
        name="password"
        self.fields[name] = forms.CharField(label=name)

    def clean(self):
        cleaned = super().clean()      
        cleaned_copy = cleaned.copy()

        for key, value in cleaned_copy.items():
            errorText = test_key(key, value)
            if errorText:
                self.add_error(key, errorText)

        return cleaned

    def save(self): 

        dict_with_username_password = self.cleaned_data
        # generate entry in db: 
        user_id = create_user(dict_with_username_password)

    def add_dynamic_field(self, name, field):
        self.fields[name] = field
    def printFields(self): 
        for name, field in self.fields.items():
            print(name, field)    


class FormField(models.Model):

    FIELD_TYPES = [
        ("char", "Textfeld (CharField)"),
        ("email", "E-Mail-Adresse"),
        ("integer", "Ganzzahl"),
        ("checkbox", "Checkbox"),
        ("textarea", "Mehrzeiliges Textfeld"),
    ]

    name = models.CharField(max_length=100, unique=True)   # Technischer Feldname
    label = models.CharField(max_length=200)               # Beschriftung
    field_type = models.CharField(
        max_length=20,
        choices=FIELD_TYPES,
    )

    required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} ({self.get_field_type_display()})"

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,        
        ordering="pub_date",
        description="Published recently? "
    )
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1) and self.pub_date <= timezone.now()
    # def tst(self, a):
    #     return a

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
