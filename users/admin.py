from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Profile

# Register your models here.
class UserAdminConfig(UserAdmin):
    search_fields = ("email", "username", "first_name", "last_name")
    list_filter = ("email", "username", "first_name", "last_name", "is_active", "is_staff", "is_superuser")
    ordering = ("-date_joined",)
    list_display = ("email", "username", "first_name", "last_name", "date_of_birth", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "username",)}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Personal", {"fields": ("first_name", "last_name", "date_of_birth")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "password1", "password2", "is_active", "is_staff")
        }),
    )


admin.site.register(Profile)
admin.site.register(Account, UserAdminConfig)

