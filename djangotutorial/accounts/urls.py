from django.contrib.auth import views as auth_views
from django.urls import path
from .views import login_or_register_view

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # path("login/", auth_views.LoginView.as_view(), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout")
    path('login/', login_or_register_view, name='login_or_register')
]