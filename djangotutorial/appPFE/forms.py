from django import forms


class LoginOrRegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# class DocumentForm(forms.Form):
#     full_name = forms.CharField(label="Vollständiger Name")
#     birth_date = forms.DateField(label="Geburtsdatum")
#     description = forms.CharField(
#         label="Beschreibung",
#         widget=forms.Textarea()
#     )
#     category = forms.ChoiceField(
#         choices=[("A", "Kategorie A"), ("B", "Kategorie B")]
#     )