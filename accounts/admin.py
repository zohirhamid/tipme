from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        "email",
        "username",
        "role",
        "is_email_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    list_filter = (
        "role",
        "is_email_verified",
        "is_staff",
        "is_active",
    )

    ordering = ("email",)
    search_fields = ("email", "username", "phone_number")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {
            "fields": ("username", "phone_number")
        }),
        ("Business", {
            "fields": ("role", "is_email_verified")
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {
            "fields": ("last_login", "created_at", "updated_at")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "phone_number",
                "role",
                "password1",
                "password2",
            ),
        }),
    )

    readonly_fields = ("created_at", "updated_at", "last_login")
