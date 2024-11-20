from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios, ModelError
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    # formulario para cambiar los datos del usuario desde el panel admin
    form = CustomUserChangeForm
    model = Usuarios
    list_display = (
        "email",
        "nombres",
        "apellidos",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active", "groups")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("nombres", "apellidos")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "nombres",
                    "apellidos",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "groups",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Usuarios, CustomUserAdmin)


class ModelErrorAdmin(admin.ModelAdmin):
    list_display = ("user", "ruta_origen", "estado", "fecha_hora_error")


admin.site.register(ModelError, ModelErrorAdmin)
