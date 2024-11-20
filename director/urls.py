from django.urls import path
from . import views


# importante la asiganicion de APPNAME para el reverso de funciones utilizando URLs
app_name = "director"


# Definicion de las rutas de la aplicacion
urlpatterns = [
    # verificacion del funcionamiento de las rutas de las aplicaciones
    # path('', views.funcionando, name='funcionando'),
    path("", views.principal_director, name="principal_director"),
    ########################################################################
    # vinculos del modulo de anteproyecto
    path("view_anteproyectos", views.view_anteproyectos, name="view_anteproyectos"),
    path("anteproyecto/<int:id>", views.anteproyecto, name="anteproyecto"),
    path(
        "eliminar_anteproyecto/<int:id>",
        views.eliminar_anteproyecto,
        name="eliminar_anteproyecto",
    ),
    path(
        "enviar_anteproyecto/<int:id>",
        views.enviar_anteproyecto,
        name="enviar_anteproyecto",
    ),
    ########################################################################
    # vinculos del modulo de proyectos
    path("view_proyectos", views.view_proyectos, name="view_proyectos"),
    path("proyecto/<int:id>", views.proyecto, name="proyecto"),
    path("enviar_proyecto/<int:id>", views.enviar_proyecto, name="enviar_proyecto"),
    path(
        "actualizar_estado_actividad/<int:actividad_id>/<int:id_proyecto>/",
        views.actualizar_estado_actividad,
        name="actualizar_estado_actividad",
    ),
    path(
        "actualizar_estado_objetivo_especifico/<int:id_proyect>/<int:id_esp>/",
        views.actualizar_estado_objetivo_especifico,
        name="actualizar_estado_objetivo_especifico",
    ),
    path(
        "enviar_observacion_objetivo/<int:id_proyect>/<int:id_esp>/",
        views.enviar_observacion_objetivo,
        name="enviar_observacion_objetivo",
    ),
    ########################################################################
    # vinculos del modulo de evaluacion de proyectos
    path(
        "evaluacion_proyectos", views.evaluacion_proyectos, name="evaluacion_proyectos"
    ),
    path(
        "view_evaluador_anteproyectos",
        views.view_evaluador_anteproyectos,
        name="view_evaluador_anteproyectos",
    ),
    path(
        "evaluar_anteproyecto/<int:id>",
        views.evaluar_anteproyecto,
        name="evaluar_anteproyecto",
    ),
    path(
        "enviar_evaluacion/<int:id>", views.enviar_evaluacion, name="enviar_evaluacion"
    ),
    path(
        "eliminar_evaluacion/<int:id>",
        views.eliminar_evaluacion,
        name="eliminar_evaluacion",
    ),
    path("view_jurado", views.view_jurado, name="view_jurado"),
    path(
        "evaluar_proyecto_final/<int:id>",
        views.evaluar_proyecto_final,
        name="evaluar_proyecto_final",
    ),
    path(
        "enviar_evaluacion_proyecto_final/<int:id>",
        views.enviar_evaluacion_proyecto_final,
        name="enviar_evaluacion_proyecto_final",
    ),
    path(
        "carga/",
        views.carga,
        name="carga",
    ),
    ########################################################################
    #     vinculos de formatos por el comite
    path("formatos_documentos", views.formatos_documentos, name="formatos_documentos"),
]
