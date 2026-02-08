from django.contrib import admin
from .models import WholeDocument  # <--- importiere dein Modell
from accounts.models import MyUser


# @admin.register(WholeDocument.user.User)
# class WholeDocumentAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in WholeDocument.user.User._meta.get_fields()]

    # list_display = ('user',)  # Alle echten Modell-Felder


# @admin.register(MyUser)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
#     list_filter = ('is_staff', 'is_superuser', 'is_active')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
