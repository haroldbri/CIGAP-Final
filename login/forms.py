# importacion de utilidades de django

from django.contrib.auth import authenticate
from .models import Usuarios
import re

from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# validacion del formulario
from django.core.exceptions import ValidationError
from django import forms

# importaciones para la creaciones de datos
# importacion de los models

# importante para editar los datos del usuario en el panel de administracio


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuarios
        fields = (
            "nombres",
            "apellidos",
            "email",
            "nombre_completo",
            "password",
            "is_active",
            "is_staff",
            "groups",
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ("nombres", "apellidos", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.set_password(self.cleaned_data["password1"])
        user.nombre_completo = f"{user.nombres} {user.apellidos}"
        if commit:
            user.save()
        return user


# creacion del formulario del registro
class FormRegistro(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ("nombres", "apellidos", "email", "password1", "password2")
        widgets = {
            "nombres": forms.TextInput(
                attrs={
                    "placeholder": "Digita tus nombres",
                    "class": "form-control",
                    "id": "inputNombre",
                }
            ),
            "apellidos": forms.TextInput(
                attrs={
                    "placeholder": "Digita tus apellidos",
                    "class": "form-control",
                    "id": "inputApellido",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "example@correo.com",
                    "class": "form-control",
                    "id": "inputCorreo",
                }
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "placeholder": "Contraseña mayor a 8 caracteres",
                    "class": "form-control",
                    "id": "id_password1",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "placeholder": "Repite la contraseña",
                    "class": "form-control",
                    "id": "id_password2",
                }
            ),
        }

    def clean_nombres(self):
        nombres = self.cleaned_data.get("nombres")
        if re.search(r"\d", nombres):
            raise ValidationError("El nombre no puede contener números.")
        if nombres.startswith(" "):
            raise ValidationError("El nombre no debe comenzar con un espacio.")
        return nombres

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get("apellidos")
        if re.search(r"\d", apellidos):
            raise ValidationError("El apellido no puede contener números.")
        if apellidos.startswith(" "):
            raise ValidationError("El apellido no debe comenzar con un espacio.")
        return apellidos

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not self.password_is_strong(password):
            raise ValidationError(
                "La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, una letra minúscula, un número y un caracter especial."
            )
        return password

    def password_is_strong(self, password):
        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"[0-9]", password)
            or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        ):
            return False
        return True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.nombres = self.cleaned_data["nombres"]
        user.apellidos = self.cleaned_data["apellidos"]
        user.nombre_completo = (
            self.cleaned_data["nombres"] + " " + self.cleaned_data["apellidos"]
        )

        if commit:
            user.save()
            estudiantes_group, created = Group.objects.get_or_create(name="Estudiantes")
            user.groups.add(estudiantes_group)
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "Contraseña mayor a 8 caracteres",
                "class": "form-control",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "Repite la contraseña",
                "class": "form-control",
            }
        )


# ya que el modelo ya esta creado, esto ya se maneja como un formulario normal


class FormEditarUsuario(forms.ModelForm):
    imagen_file = forms.ImageField(
        required=False,
        label="Imagen de usuario",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )
    current_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese su contraseña actual",
            }
        ),
        required=False,
    )
    password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Ingrese nueva contraseña"}
        ),
        required=False,
    )
    password2 = forms.CharField(
        label="Confirma la nueva contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirme nueva contraseña"}
        ),
        required=False,
    )

    class Meta:
        model = Usuarios
        fields = (
            "nombres",
            "apellidos",
            "email",
            "imagen_file",
            "current_password",
            "password1",
            "password2",
        )
        widgets = {
            "nombres": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese sus nombres"}
            ),
            "apellidos": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese sus apellidos"}
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese su correo electrónico",
                }
            ),
            "imagen_file": forms.FileInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Verificar que la contraseña actual sea correcta
        if current_password:
            if not self.instance.check_password(current_password):
                self.add_error(
                    "current_password", "La contraseña actual es incorrecta."
                )

        # Verificar que las nuevas contraseñas coincidan
        if password1 and password1 != password2:
            self.add_error("password2", "Las nuevas contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Manejo de la imagen manualmente
        if self.cleaned_data.get("imagen_file"):
            user.imagen = self.cleaned_data["imagen_file"].read()

        # Cambio de contraseña
        password1 = self.cleaned_data.get("password1")
        if password1:
            user.set_password(password1)

        if commit:
            user.save()
        return user
