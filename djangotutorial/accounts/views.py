from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import RedirectView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from .forms import LoginOrRegisterForm
from .models import MyUserData

from django.urls import reverse_lazy

class IndexView(RedirectView):
    # url = reverse_lazy('accounts:login')  
    url = reverse_lazy('accounts:login_or_register')  
    # template_name = "accounts/index.html"

    # def get_context_data(self, **kwargs):
    #     return redirect("accounts:login")
    #     context = super().get_context_data(**kwargs)
    #     return context


def login_or_register_view(request):
    if request.method == "POST":
        form = LoginOrRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                my_user = MyUserData.objects.get(username=username)
                # User existiert → Passwort checken
                if my_user.check_password(password):
                    # Optional: Django Auth User existiert? Dann Session setzen
                    user, created = User.objects.get_or_create(username=username)
                    login(request, user)
                    return redirect('appPFE:docForm')
                else:
                    messages.error(request, "Falsches Passwort")
            except MyUserData.DoesNotExist:
                # User existiert nicht → erstellen
                my_user = MyUserData(username=username)
                my_user.set_password(password)
                # Optional auch Django User erstellen
                user, created = User.objects.get_or_create(username=username)
                login(request, user)
                return redirect('appPFE:docForm')
    else:
        form = LoginOrRegisterForm()

    return render(request, "registration/login_or_register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')  # oder wohin auch immer