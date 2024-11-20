from django.shortcuts import redirect

# unica importacion para manejar el LogOut de las cuentas
from django.contrib.auth import logout
from django.shortcuts import render
from login.models import ModelError
import datetime


def logout_user(request):
    logout(request)
    return redirect("login:loginapps")


# def errors(request):
#     return render(request, 'errors.html')


errores = {
    "404": {
        "num_error": "404",
        "mensaje": "La página solicitada <b>no fue encontrada</b>. Esto puede suceder si la <b>URL está mal escrita</b>, si la página <b>ha sido eliminada o si se esta intentando <b>acceder sin sesión</b> tomando una nueva redirección de URL.</b>",
    },
    "401": {
        "num_error": "401",
        "mensaje": "<b>Es necesario autenticarse</b> para acceder a esta página. Por favor, <b>inicia sesión</b> e inténtalo de nuevo.",
    },
    "400": {
        "num_error": "400",
        "mensaje": "La solicitud <b>enviada al servidor es incorrecta</b> o no puede ser procesada. <b>Verifica la URL o los datos enviados</b> e inténtalo de nuevo.",
    },
    "403": {
        "num_error": "403",
        "mensaje": "<b>No tienes permiso para acceder</b> al recurso solicitado. <b>Verifica tus credenciales</b> o contacta con el administrador del sitio.",
    },
    "500": {
        "num_error": "500",
        "mensaje": "Ha ocurrido un <b>problema en el servidor</b> o <b>no tienes acceso a este usuario</b>, lo que impide procesar la solicitud correctamente. <b>Intenta nuevamente más tarde.</b>",
    },
}


def handler404(request, exception):
    return render(request, "errors.html", errores["404"])


def handler400(request, exception):

    return render(request, "errors.html", errores["400"])


# manejo del token

# recordar que como este es personalizado respecto al error del token, se instancion en el settings


def csrf_failure(request, reason=""):
    return render(request, "errors.html", errores["403"], status=403)


# def handler403(request, exception=None):
#     return render(request, 'errors.html', errores['403'], status=403)

# esta no maneja excepcion


# import traceback

# def handler500(request):
#     error_message = traceback.format_exc()
#     errores["500"]["detalle"] = error_message
#     return render(request, "errors.html", errores["500"])
# def handler500(request):
#     return render(request, "errors.html", errores["500"])


# def handler401(request,exception):
#     return render(request, 'errors.html', errores['401'])


def handler500(request):
    return render(request, "errors.html", errores["500"])


# def handler401(request,exception):
#     return render(request, 'errors.html', errores['401'])


def submit_error(request):
    ruta_origen = request.META.get("HTTP_REFERER", "Desconocido")
    if request.method == "POST":
        codigo = request.POST.get("estado")

        print(f"Estado recibido: {codigo}")

        model = ModelError(
            user=request.user,
            estado=int(codigo),
            ruta_origen=ruta_origen,
            fecha_hora_error=datetime.datetime.now(),
        )

        model.save()
        logout(request)
        return redirect("login:loginapps")
    else:
        logout(request)
        return redirect("login:loginapps")
