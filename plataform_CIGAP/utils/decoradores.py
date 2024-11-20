

# Es este script vamos a crear un decroador el cual va a poner un filtro de usuarios que inician secion.
# esto con el fin de controlar el acceso a otras aplicaciones por medio de las url, estas solo por permiciones de grupos


from django.contrib import messages
from django.http import HttpResponse

from plataform_CIGAP.views import handler404


def grupo_usuario(nombre_grupo):
    def decorador(view):
        def view_envuelta(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.groups.filter(name=nombre_grupo).exists():
                    return view(request, *args, **kwargs)
                else:

                    return handler404

            else:

                return HttpResponse('Error, el usuario no esta autenticado.')
                # return redirect
        return view_envuelta
    return decorador


# def grupo_usuario(nombre_grupo):
#     def decorador(view):
#         def view_envuelta(request, *args, **kwargs):
#             if request.user.is_authenticated:
#                 if request.user.groups.filter(name=nombre_grupo).exists():
#                     return view(request, *args, **kwargs)
#                 else:

#                     messages.error(
#                         request, "No tiene permisos para acceder a esta sección.")
#                     return redirect('nombre_de_la_vista_de_permiso')
#             else:

#                 messages.error(
#                     request, "Error: debe iniciar sesión para acceder a esta sección.")

#                 return redirect('login:loginapps')

#         return view_envuelta
#     return decorador
