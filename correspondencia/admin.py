from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ModelFechasComite,
    ModelRetroalimentaciones,
    ModelAsignacionJurados,
    ModelInformacionEntregaFinal,
    ModelSolicitudes,
    ModelDocumentos,
)
import base64

# Register your models here.

# Registro del modelo de retroalimentaciones en el panel admin


class ModelRetroalimentacionesAdmin(admin.ModelAdmin):
    list_display = (
        "anteproyecto",
        "proyecto_final",
        "retroalimentacion",
        "fecha_retroalimentacion",
        "estado",
        "revs_dadas",
        "doc_retroalimentacion_link",
    )

    def doc_retroalimentacion_link(self, obj):
        if obj.doc_retroalimentacion:
            if isinstance(obj.doc_retroalimentacion, bytes):
                base64_data = base64.b64encode(obj.doc_retroalimentacion).decode("utf8")
                url = f"data:application/octet-stream;base64,{base64_data}"
                if obj.anteproyecto:
                    nombre_anteproyecto = obj.anteproyecto.nombre_anteproyecto
                else:
                    nombre_anteproyecto = "Desconocido"
                return format_html(
                    '<a href="{}" download="{}">Descargar Carta de Presentación</a>',
                    url,
                    f"Retroalimentacion_{nombre_anteproyecto}.pdf",
                )
        return "No Cargado"

    doc_retroalimentacion_link.short_description = "Documento retroalimentado"


admin.site.register(ModelRetroalimentaciones, ModelRetroalimentacionesAdmin)


@admin.register(ModelAsignacionJurados)
class ModelAsignacionJuradosAdmin(admin.ModelAdmin):
    list_display = ("proyecto_final", "nombre_jurado", "fecha_sustentacion")
    search_fields = ("proyecto_final__anteproyecto__nombre_anteproyecto",)
    list_filter = ("fecha_sustentacion",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "anteproyecto",
                    "proyecto_final",
                    "fecha_sustentacion",
                )
            },
        ),
    )


# Registro del modelo de Informacion de entrega Final de jurados en el panel admin
from django.contrib import admin  # type: ignore
from .models import ModelInformacionEntregaFinal


@admin.register(ModelInformacionEntregaFinal)
class ModelInformacionEntregaFinalAdmin(admin.ModelAdmin):
    list_display = (
        "anteproyecto",
        "proyecto_final",
        "fecha_finalizacion",
    )
    search_fields = ("anteproyecto__nombre", "proyecto_final__nombre")
    list_filter = ("fecha_finalizacion",)
    readonly_fields = ("doc_proyecto_final_cedido",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "anteproyecto",
                    "proyecto_final",
                    "fechas_proyecto",
                    "fecha_finalizacion",
                    "doc_proyecto_final_cedido",
                )
            },
        ),
    )


# registro del modelo de solicitudes especificas
admin.site.register(ModelSolicitudes)
# registro del modele de formatos
admin.site.register(ModelDocumentos)


@admin.register(ModelFechasComite)
class ModelFechasComiteAdmin(admin.ModelAdmin):
    list_display = (
        "ano_actual",
        "periodo_academico",
        "primer_encuentro",
        "segundo_encuentro",
        "tercer_encuentro",
        "cuarto_encuentro",
        "extraordinaria",
    )
    search_fields = ("ano_actual", "periodo_academico")
    list_filter = ("periodo_academico",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "ano_actual",
                    "periodo_academico",
                    "primer_encuentro",
                    "segundo_encuentro",
                    "tercer_encuentro",
                    "cuarto_encuentro",
                    "extraordinaria",
                )
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        return form
