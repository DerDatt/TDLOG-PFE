from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import RedirectView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import LoginOrRegisterForm
from .models import MyUser

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

    if request.user.is_authenticated:
        logout(request)
        
    if request.method == "POST":
        form = LoginOrRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # user exists and password is correct
                login(request, user)
                return redirect('appPFE:docForm')
            else:
                # user does not exist or wrong password
                try:
                    MyUser.objects.get(username=username)
                    # user exists → wrong password
                    messages.error(request, "Wrong password")
                except MyUser.DoesNotExist:
                    # user does not exist → create new user
                    user = MyUser.objects.create_user(
                        username=username,
                        password=password
                    )
                    login(request, user)

                    # mark user as new
                    request.session['is_new_user'] = True

                    return redirect('appPFE:docForm')


            # try:
            #     my_user = MyUserData.objects.get(username=username)
            #     # User existiert → Passwort checken
            #     if my_user.check_password(password):
            #         # Optional: Django Auth User existiert? Dann Session setzen
            #         user, created = User.objects.get_or_create(username=username)
            #         login(request, user)
            #         return redirect('appPFE:docForm')
            #     else:
            #         messages.error(request, "Falsches Passwort")
            # except MyUserData.DoesNotExist:
            #     # User existiert nicht → erstellen
            #     my_user = MyUserData(username=username)
            #     my_user.set_password(password)
            #     # Optional auch Django User erstellen
            #     user, created = User.objects.get_or_create(username=username)
            #     login(request, user)
            #     return redirect('appPFE:docForm')
    else:
        form = LoginOrRegisterForm()

    return render(request, "registration/login_or_register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')  # oder wohin auch immer