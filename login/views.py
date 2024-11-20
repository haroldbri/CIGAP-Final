# Asegúrate de que la ruta de importación sea correcta
from plataform_CIGAP.settings import base_dir
from .models import Usuarios  # Asegúrate de importar tu modelo
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# import pythoncom
# import win32com.client as win32
from django.conf import settings
import requests
from .models import Usuarios  # Asegúrate de importar tu modelo Usuarios
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .forms import FormRegistro
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.crypto import get_random_string
import re

# Create your views here.


from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

# from django.contrib.auth.models import User
# importacion de los models


from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

from .forms import FormRegistro, FormEditarUsuario


# importacion para la codificacion de las imagenes
import base64

# importacion de modelo de usuarios
from .models import Usuarios


# utilidades
def existe_usuario(email):
    usuario = (
        Usuarios.objects.get(email=email)
        if Usuarios.objects.filter(email=email).exists()
        else None
    )
    if not usuario:
        return None
    return True


# Creacion de la vista global del login
def loginapps(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        print(f"Username: {username}, Password: {password}")
        user = authenticate(request, username=username, password=password)
        print(f"Authenticated User: {user}")

        if user is not None:
            print("User is authenticated")
            auth_login(request, user)
            user_groups = user.groups.values_list("name", flat=True)
            print(f"User Groups: {user_groups}")
            if "Estudiantes" in user_groups:
                messages.success(request, "Bienvenido, Estudiante!")
                return redirect("estudiante:principal_estudiante")
            elif "Directores" in user_groups:
                messages.success(request, "Bienvenido, Director!")
                return redirect("director:principal_director")
            elif "Correspondencia" in user_groups:
                messages.success(request, "Bienvenido, Correspondencia!")
                return redirect("correspondencia:principal_correspondencia")
            else:
                return HttpResponse("No tienes acceso a ninguna sección.")
        else:
            messages.error(
                request, "Verifique que el correo y la contraseña sean correctos."
            )
            return redirect("login:loginapps")

    else:
        form = FormRegistro
        return render(request, "login.html", {"form": form})


def registro(request):
    if request.method == "POST":
        form = FormRegistro(request.POST)
        email = form.data.get("email")
        existe = existe_usuario(email)

        if existe:
            messages.error(
                request,
                f"Error en el registro. El correo electrónico {email} ya se encuentra registrado.",
            )
            return redirect("login:loginapps")

        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"El usuario {user.email} ha sido registrado exitosamente."
            )
            return redirect("login:loginapps")
        else:

            password1_errors = form.errors.get("password1", [])
            password2_errors = form.errors.get("password2", [])
            if password1_errors:
                messages.error(
                    request, f"Error en el registro. {' '.join(password1_errors)}"
                )
            if password2_errors:
                messages.error(
                    request, f"Error en el registro. {' '.join(password2_errors)}"
                )
            return redirect("login:loginapps")
    else:
        return redirect("login:loginapps")


# esta es la funcion que permite cambiar los datos de cada uno de los estudiantes
def editar_usuario(request):
    usuario = request.user
    # recuperacion de la imagen propia del usuaario en formato binario
    # print(imagen, 'esta es la imagen')
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(imagen).decode("utf-8") if imagen else ""

    if request.method == "POST":
        form = FormEditarUsuario(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            user = form.save()

            # revizar esta logica
            # Autenticar de nuevo al usuario si el correo electrónico ha cambiado
            if user.email != request.user.email:
                auth_login(request, user)
            user_groups = user.groups.values_list("name", flat=True)
            if "Estudiantes" in user_groups:
                return redirect("estudiante:principal_estudiante")
            elif "Directores" in user_groups:
                return redirect("director:principal_director")
            elif "Correspondencia" in user_groups:
                return redirect("correspondencia:principal_correspondencia")
            else:
                return HttpResponse("No tienes acceso a ninguna seción")
            return redirect("director:base_director")
        else:
            return render(
                request,
                "director/base_director.html",
                {
                    "form_config": form,
                    "usuario": usuario,
                    "user_img": imagen_convertida,
                },
            )


def recuperar_cuenta(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            user = (
                Usuarios.objects.get(email=email)
                if Usuarios.objects.filter(email=email).exists()
                else None
            )
            if user:
                token = get_random_string(length=32)
                user.token = token
                user.save()
                recovery_link = request.build_absolute_uri(
                    reverse("login:recuperar_cuenta_confirm", args=[token])
                )
                context["link_recuperar"] = recovery_link
                context["usuario"] = {
                    "email": email,
                    "nombre_completo": user.nombre_completo,
                }
                messages.success(
                    request,
                    "Se ha enviado un enlace de recuperación a tu correo electrónico. Espera unos segundos.",
                )
                return render(request, "recuperar_cuenta.html", context)
            else:
                messages.error(
                    request,
                    f"El email {email} no esta registrado en la plataforma, verifica de nuevo.",
                )
                return render(request, "login.html")
        else:

            messages.error(
                request,
                f"El email {email} no esta registrado en la plataforma, verifica de nuevo.",
            )
            return render(request, "recuperar_cuenta.html")

    return render(request, "recuperar_cuenta.html")


# def recuperar_cuenta(request):

#     pythoncom.CoInitialize()

#     if request.method == "POST":
#         email = request.POST.get("email")

#         try:
#             user = Usuarios.objects.get(email=email)
#             token = get_random_string(length=32)
#             user.token = token
#             user.save()

#             recovery_link = request.build_absolute_uri(
#                 reverse("login:recuperar_cuenta_confirm", args=[token])
#             )

#             # Configurar Outlook
#             outlook = win32.Dispatch("outlook.application")

#             # Configurar los detalles del correo
#             asunto = "Recuperación de cuenta"
#             cuerpo_html = f"""
#             <div style="font-family: 'Saira', sans-serif; border-radius: 10px; padding: 20px; background-color: #002412; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); max-width: 600px; margin: 0 auto;">
#                 <div style="background: #ffffff; border-radius: 12px;">
#                     <header style="width: 100%; display: flex; background: #ffffff; padding: 0; border-radius: 10px 10px 0 0; align-items: center; justify-content: center;">
#                         <img src="https://upload.wikimedia.org/wikipedia/commons/1/11/Logo_Universidad_de_Cundinamarca.png" alt="Logo Universidad de Cundinamarca" style="margin: 0 auto; padding: 8px; z-index: 0; max-width: 100%; max-height: 165px;">
#                     </header>
#                     <h1 style="width: 100%; background-color: #002412; margin: 0; padding: 12px 0; text-align: center; color: #ffffff; margin-bottom: 20px;">Plataforma CIGAP Ubaté</h1>
#                     <h2 style="color: #000000;padding: 0 12px;">Recuperación de contraseña para <span style="font-weight: bold;">{email}</span></h2>
#                     <p style="padding: 0 12px; color: #666666;">Hola <span style="color: #007A3D; font-weight: bold;">{user.nombres}</span>, has solicitado la recuperación de tu contraseña para la cuenta creada con el correo <span style="color: #007A3D; font-weight: bold;">{email}</span>.</p>
#                     <p style="padding: 0 12px; color: #666666;">Para restablecer tu contraseña, haz clic en el siguiente enlace: <a href="{recovery_link}" style="color: #007A3D; text-decoration: none;">Recuperar cuenta</a></p>
#                     <p style="padding: 0 12px; color: #666666;">Recuerda que la protección de tus datos es importante, puedes cambiar tu contraseña accediendo a la plataforma.</p>
#                     <h3 style="padding: 0 12px; color: #000000;">Estaremos en contacto.</h3>
#                     <div style="width: 100%; background: #3C3C3B; padding: 0; border-radius: 0 0 10px 10px;">
#                         <div style="padding: 8px;">
#                             <h2 style="color: #fff; margin-bottom: 5px; font-weight: 600; text-align: center;">Respuesta automática de la plataforma <br> CIGAP</h2>
#                             <p style="color: #fff; margin-top: 5px; text-align: center; font-size: 12px;">No responder a este correo.</p>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#             """

#             # Crear y enviar el mensaje
#             mail = outlook.CreateItem(0)
#             mail.To = email
#             mail.Subject = asunto
#             mail.HTMLBody = cuerpo_html

#             # Enviar el correo
#             mail.Send()

#             messages.success(
#                 request,
#                 "Se ha enviado un enlace de recuperación a tu correo electrónico.",
#             )
#             return redirect("login:loginapps")

#         except Usuarios.DoesNotExist:
#             messages.error(request, "No existe un usuario con ese correo electrónico.")

#         except Exception as e:
#             messages.error(
#                 request,
#                 f"Hubo un error al enviar el correo de recuperación: {str(e)}. Por favor, intenta nuevamente.",
#             )
#             return render(request, "recuperar_cuenta.html")

#     return render(request, "recuperar_cuenta.html")


def validar_contrasena(contrasena, user):
    if len(contrasena) < 8:
        return "La contraseña debe contener al menos 8 caracteres."

    if (
        user.nombres.lower() in contrasena.lower()
        or user.apellidos.lower() in contrasena.lower()
        or user.email.lower() in contrasena.lower()
    ):
        return "La contraseña no debe ser demasiado similar a tu información personal."

    contrasenas_comunes = ["12345678", "password", "qwerty"]
    if contrasena in contrasenas_comunes:
        return "La contraseña no debe ser una contraseña comúnmente utilizada."

    if not (
        re.search(r"[A-Za-z]", contrasena)
        and re.search(r"\d", contrasena)
        and re.search(r"[^\w\s]", contrasena)
    ):
        return (
            "La contraseña debe incluir una combinación de letras, números y símbolos."
        )

    return None


def recuperar_cuenta_confirm(request, token):
    if request.method == "POST":
        nueva_contrasena = request.POST.get("nueva_contrasena")
        confirmar_contrasena = request.POST.get("confirmar_contrasena")

        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, "Las contraseñas no coinciden. Inténtalo de nuevo.")
        else:
            try:
                user = Usuarios.objects.get(token=token)
                user.token = None
                error = validar_contrasena(nueva_contrasena, user)
                if error:
                    messages.error(request, error)

                user.set_password(nueva_contrasena)
                user.save()
                messages.success(request, "Tu contraseña ha sido actualizada.")
                return redirect("login:loginapps")

            except Usuarios.DoesNotExist:
                messages.error(request, "El token de recuperación es inválido.")

    return render(request, "recuperar_cuenta_confirm.html", {"token": token})


# resend.api_key = "re_i2AKGn92_3GqGVCbZP4y8sw3Ash4xEsKM"
# def recuperar_cuenta(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')

#         try:
#             user = Usuarios.objects.get(email=email)  # Usa tu modelo Usuarios
#             token = get_random_string(length=32)  # Generar un token único
#             user.token = token  # Asigna el token al usuario
#             user.save()  # Guarda el usuario con el token

#             # Crear el enlace de recuperación
#             recovery_link = request.build_absolute_uri(
#                 reverse('login:recuperar_cuenta_confirm', args=[token])
#             )

#             # Intentar enviar el correo electrónico usando Resend
#             try:
#                 r = resend.Emails.send({
#                     "from": "onboarding@resend.dev",  # Cambia esto por tu correo de remitente
#                     "to": 'plataformaCIGAPUbate@outlook.com',  # Correo electrónico del destinatario
#                     "subject": "Recuperación de cuenta",
#                     "html": f"<p>Haz clic en el siguiente enlace para recuperar tu cuenta: <a href='{recovery_link}'>Recuperar cuenta</a></p>",
#                 })
#                 messages.success(
#                     request, 'Se ha enviado un enlace de recuperación a tu correo electrónico.')
#                 return redirect('login:loginapps')
#             except Exception as e:  # Captura cualquier excepción al enviar el correo
#                 messages.error(
#                     request, f'Hubo un error al enviar el correo de recuperación: {str(e)}. Por favor, intenta nuevamente.')
#                 return render(request, 'recuperar_cuenta.html')

#         except Usuarios.DoesNotExist:  # Cambiar User por Usuarios
#             messages.error(
#                 request, 'No existe un usuario con ese correo electrónico.')
#     return render(request, 'recuperar_cuenta.html')
