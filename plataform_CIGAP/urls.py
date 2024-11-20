from . import views

"""
URL configuration for plataform_CIGAP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#  """"asi esta"""
# configuracion del logout de las cuentas
from django.contrib.auth import views as auth_views
from .views import handler400, logout_user, errores
from django.views.csrf import csrf_failure


urlpatterns = [
    path("admin/", admin.site.urls),
    path("estudiante/", include("estudiante.urls")),
    path("director/", include("director.urls")),
    path("correspondencia/", include("correspondencia.urls")),
    path("", include("login.urls")),
    # vista y url del logout
    path("logout/", views.logout_user, name="logout_user"),
    path("submit_error/", views.submit_error, name="submit_error"),
    # ruta de errores
    # path('errors/', views.errors, name='errors'),
]

# vistas de manejo de errores
handler400 = "plataform_CIGAP.views.handler400"
handler500 = "plataform_CIGAP.views.handler500"
# handler401 = 'plataform_CIGAP.views.handler401'
# handler403 = 'plataform_CIGAP.views.handler403'
handler404 = "plataform_CIGAP.views.handler404"
