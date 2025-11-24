import datetime
from sqlite3 import adapt

from django.db import models
from django.utils import timezone
from django.contrib import admin 
from django import forms

import pandas as pd

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    message2 = models.TextField()
    tstfield = models.TimeField(verbose_name="Manually Set name", auto_now=False, auto_now_add=False)
    field2 = models.FileField(upload_to=None, max_length=100)
    field3 = models.FilePathField() #(""), path=None, match=None, recursive=recursive, max_length=100)

    def __str__(self):
        return self.name


class WholeDocument(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path_csv = "appPFE/field_data.csv"

        df = pd.read_csv(self.path_csv)

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
                values_ab_spalte_3 = [
                    row[col] for col in df.columns[2:] if pd.notna(row[col])
                ]
                choices = [(value, value) for value in values_ab_spalte_3]
                field = forms.ChoiceField(label=name, choices=choices)
            else:
                print("ERROR IN FILETYPE")
            if field:
                self.fields[name] = field

    def test_if_valid(self):
        # do function from Vincent
        self.cleaned_data
        
    def save(self): 
        print(self.cleaned_data)
        

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
