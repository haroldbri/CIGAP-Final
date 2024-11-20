from django.urls import path
from . import views

# importante la asiganicion de APPNAME para el reverso de funciones utilizando URLs
app_name = "estudiante"


# Definicion de las rutas de la aplicacion
urlpatterns = [
    # verificacion del funcionamiento de las rutas de las aplicaciones
    # path('', views.funcionando, name='funcionando'),
    path("", views.principal_estudiante, name="principal_estudiante"),
    # path('estudiante', views.estudiante, name='estudiante'),
    #!funcionando
    path("solicitud", views.solicitud, name="solicitud"),
    path(
        "actualizar_documentos_anteproyecto/<int:id>",
        views.actualizar_documentos_anteproyecto,
        name="actualizar_documentos_anteproyecto",
    ),
    path("info_proyect/", views.info_proyect, name="info_proyect"),
    path(
        "enviar_solicitud_proyecto/",
        views.enviar_solicitud_proyecto,
        name="enviar_solicitud_proyecto",
    ),
    path(
        "solicitudes_especificas/",
        views.solicitudes_especificas,
        name="solicitudes_especificas",
    ),
    ################################################################################
    path("avances_proyecto/", views.avances_proyecto, name="avances_proyecto"),
    path(
        "cargar_docs_final/<int:id_proyecto>",
        views.cargar_docs_final,
        name="cargar_docs_final",
    ),
    path(
        "modificar_docs_final/<int:id_proyecto>",
        views.modificar_docs_final,
        name="modificar_docs_final",
    ),
    path(
        "subir_objetivo_general/<int:id>",
        views.subir_objetivo_general,
        name="subir_objetivo_general",
    ),
    path(
        "editar_objetivo_general/<int:id>",
        views.editar_objetivo_general,
        name="editar_objetivo_general",
    ),
    path(
        "subir_objetivo_especifico/<int:id>",
        views.subir_objetivo_especifico,
        name="subir_objetivo_especifico",
    ),
    path(
        "eliminar_objetivo_general/<int:id>",
        views.eliminar_objetivo_general,
        name="eliminar_objetivo_general",
    ),
    path(
        "editar_objetivo_especifico/<int:id>",
        views.editar_objetivo_especifico,
        name="editar_objetivo_especifico",
    ),
    path(
        "eliminar_objetivo_especifico/<int:id>",
        views.eliminar_objetivo_especifico,
        name="eliminar_objetivo_especifico",
    ),
    path(
        "editar_eliminar_archivo/<int:id>",
        views.editar_eliminar_archivo,
        name="editar_eliminar_archivo",
    ),
    path(
        "subir_actividad/<int:id_proyecto>/<int:id_esp>",
        views.subir_actividad,
        name="subir_actividad",
    ),
    path("editar_actividad/<int:id>", views.editar_actividad, name="editar_actividad"),
    path(
        "eliminar_actividad/<int:id>",
        views.eliminar_actividad,
        name="eliminar_actividad",
    ),
    path("subir_avance/<int:id_esp>", views.subir_avance, name="subir_avance"),
    path(
        "cargar_editar_documento_cedido/<int:id>",
        views.cargar_editar_documento_cedido,
        name="cargar_editar_documento_cedido",
    ),
    ################################################################################
    path("formatos_documentos/", views.formatos_documentos, name="formatos_documentos"),
]
