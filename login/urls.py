from . import views


from django.contrib import admin
from django.urls import path, include
app_name = 'login'


urlpatterns = [
    #  ruta de registro para el patterns de la app
    path('', views.loginapps, name='loginapps'),
    path('registro', views.registro, name='registro'),
    path('recuperar_cuenta', views.recuperar_cuenta, name='recuperar_cuenta'),
     path('recuperar_cuenta_confirm/<str:token>/', views.recuperar_cuenta_confirm, name='recuperar_cuenta_confirm'),
    path('editar_usuario', views.editar_usuario, name='editar_usuario'),
]
