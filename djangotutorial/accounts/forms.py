# This app contains the Custom User Model (MyUser) and related forms
from django import forms


class LoginOrRegisterForm(forms.Form):
    """Form for user login or registration"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
