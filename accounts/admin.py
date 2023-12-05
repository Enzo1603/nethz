from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = UserAdmin.list_display
    fieldsets = fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "email")},
        ),
        ("Worldle Stats", {"fields": ("areas_highscore",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets


admin.site.register(CustomUser, CustomUserAdmin)
