from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "message", "message2" , "tstfield", "field2"]# , "field3"]#, "tstfield", "field2"]

class DocumentForm(forms.Form):
    full_name = forms.CharField(label="Vollständiger Name")
    birth_date = forms.DateField(label="Geburtsdatum")
    description = forms.CharField(
        label="Beschreibung",
        widget=forms.Textarea()
    )
    category = forms.ChoiceField(
        choices=[("A", "Kategorie A"), ("B", "Kategorie B")]
    )