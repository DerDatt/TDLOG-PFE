import datetime
from sqlite3 import adapt

from django.db import models
from django.utils import timezone
from django.contrib import admin 
from django import forms

import pandas as pd

from .convertisseur import test_nom, test, test_normes, get_test_data

from .generate_text import generate_pdf_file


class WholeDocument(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fill_fields_with_csv()

    def fill_fields_with_csv(self):
        path_csv = "appPFE/field_data.csv"
        df = pd.read_csv(path_csv)
        for _, row in df.iterrows():
            name = row["name"]
            field_type = row["field_type"]

            field = None
            if field_type == "text_field":
                field = forms.CharField(label=name)
            elif field_type == "checkbox":
                field = forms.BooleanField(label=name, required=False)
            elif field_type == "image_field":
                field = forms.ImageField(label=name, allow_empty_file=True)
            elif field_type == "choice_field":
                # Werte ab Spalte 3 (indexbasiert: 2) einsammeln und als Choice-Paare aufbereiten.
                values_from_col_3 = [
                    row[col] for col in df.columns[2:] if pd.notna(row[col])
                ]
                choices = [(value, value) for value in values_from_col_3]
                field = forms.ChoiceField(label=name, choices=choices)
            else:
                print("ERROR IN FILETYPE")
            if field:
                self.fields[name] = field



    def clean___Prenom_NOM__(self):
        value = self.cleaned_data.get("__Prenom_NOM__")

        if not test_nom(value):
            raise forms.ValidationError("Name not good")

        return value


    def clean___Presentation_missions_FR__(self):
        value = self.cleaned_data.get("__Presentation_missions_FR__")

        if not "mission" in value:
            raise forms.ValidationError("The word \"mission\" must occur")

        return value

    def clean(self):
        cleaned = super().clean()        
        key = "__Promotion__"
        val = cleaned.get(key)
        if not val.isdigit():
            self.add_error(key, "Promotion must be a number. ")
        elif int(val) > 30:
            self.add_error(key, "Promotion is maximal 30")
        

        # this can become for loop over keys
        key = "__Titre_PFE_FR__"
        val = cleaned.get(key)
        errorText = test(key, val)
        if errorText:
            self.add_error(key, errorText)

        return cleaned


    def test_if_valid(self):
        # do function from Vincent
        data = get_test_data()
        for j in self.cleaned_data.keys():
            data[j] = self.cleaned_data[j]

        data = self.cleaned_data

        # print("- - - data: - - -")
        # print(data)
        # print("- - - data end: - - -")
        # print("- - - tests: - - -")
        # print(test_normes(data))
        # print("- - - tests end: - - -")
        
    def save(self): 

        d = self.cleaned_data

        # call function in generate_text.py: 
        generate_pdf_file(d)

        pass # print(self.cleaned_data)
        

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
