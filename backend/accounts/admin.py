from django.contrib import admin
from .models import MyUser


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'form_complete')
    # fields = ('username', 'password', 'is_staff')
    # Admin kann nur diese Felder angeben

    # list_filter = ('is_staff', 'is_superuser', 'is_active')
    # search_fields = ('username')

    # Dynamische Felder im Add-Formular

    def get_fieldsets(self, request, obj=None):
        if obj is None:  # Add-Form
            if request.user.is_superuser:
                return (
                    (None, {
                        'classes': ('wide',),
                        'fields': ('username', 'password', 'is_staff'),
                    }),
                )
            else:  # Staff
                return (
                    (None, {
                        'classes': ('wide',),
                        'fields': ('username', 'password'),
                    }),
                )
        else:
            # Edit-Form (obj existiert) → normale Felder
            return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        """Hash the password when set in the admin form (add or change)."""
        raw_password = form.cleaned_data.get("password")
        if raw_password:
            obj.set_password(raw_password)
        super().save_model(request, obj, form, change)
