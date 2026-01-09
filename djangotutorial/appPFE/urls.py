from django.urls import path

from . import views

app_name = "appPFE"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.IndexView.as_view(), name="index"),
    # path("contact/", views.contact_view, name="contact"),
    path("login_form/", views.login_view, name="loginForm"),
    path("doc_form/", views.doc_view, name="docForm"),
    path("success/", views.success_view, name="success"),
    path("translate/", views.translate_view, name='translate')
]