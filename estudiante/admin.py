import base64
from .models import (
    ModelAnteproyecto,
    ModelProyectoFinal,
    ModelObjetivoGeneral,
    ModelObjetivosEspecificos,
    ModelActividades,
    ModelFechasProyecto,
)
from django.contrib import admin
from django.utils.html import format_html


class ModelAnteproyectoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_anteproyecto",
        "nombre_integrante1",
        "nombre_integrante2",
        "director",
        "codirector",
        "carta_presentacion_link",
        "anteproyecto_link",
    )

    def carta_presentacion_link(self, obj):
        if obj.carta_presentacion and isinstance(obj.carta_presentacion, bytes):
            base64_data = base64.b64encode(obj.carta_presentacion).decode("utf-8")
            url = f"data:application/octet-stream;base64,{base64_data}"
            return format_html(
                '<a href="{url}" download="{filename}">Descargar Carta de Presentación</a>',
                url=url,
                filename="carta_presentacion.pdf",
            )
        return "No cargado"

    carta_presentacion_link.short_description = "Carta de Presentación"

    def anteproyecto_link(self, obj):
        if obj.anteproyecto and isinstance(obj.anteproyecto, bytes):
            base64_data = base64.b64encode(obj.anteproyecto).decode("utf-8")
            url = f"data:application/octet-stream;base64,{base64_data}"
            return format_html(
                '<a href="{url}" download="{filename}">Descargar Anteproyecto</a>',
                url=url,
                filename="anteproyecto.pdf",
            )
        return "No cargado"

    anteproyecto_link.short_description = "Anteproyecto"


admin.site.register(ModelAnteproyecto, ModelAnteproyectoAdmin)


class ModelProyectoFinalAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "anteproyecto",
        "fecha_envio",
        "solicitud_enviada",
        "estado",
        "carta_presentacion_final_link",
        "proyecto_final_link",
    )

    def carta_presentacion_final_link(self, obj):
        if obj.carta_presentacion_final and isinstance(obj.carta_presentacion_final, bytes):
            base64_data = base64.b64encode(obj.carta_presentacion_final).decode("utf-8")
            url = f"data:application/octet-stream;base64,{base64_data}"
            return format_html(
                '<a href="{url}" download="carta_presentacion_final.pdf">Descargar Carta de Presentación Final</a>',
                url=url,
            )
        return "No cargado"

    carta_presentacion_final_link.short_description = "Carta de Presentación Final"

    def proyecto_final_link(self, obj):
        if obj.proyecto_final and isinstance(obj.proyecto_final, bytes):
            base64_data = base64.b64encode(obj.proyecto_final).decode("utf-8")
            url = f"data:application/octet-stream;base64,{base64_data}"
            return format_html(
                '<a href="{url}" download="proyecto_final.pdf">Descargar Proyecto Final</a>',
                url=url,
            )
        return "No cargado"

    proyecto_final_link.short_description = "Proyecto Final"


admin.site.register(ModelProyectoFinal, ModelProyectoFinalAdmin)


@admin.register(ModelObjetivoGeneral)
class ModelObjetivoGeneralAdmin(admin.ModelAdmin):
    list_display = ("proyecto_final", "descripcion")
    search_fields = ("descripcion",)


@admin.register(ModelObjetivosEspecificos)
class ModelObjetivosEspecificosAdmin(admin.ModelAdmin):
    list_display = ("objetivo_general", "descripcion", "estado")
    search_fields = ("descripcion",)
    list_filter = ("estado",)


@admin.register(ModelActividades)
class ModelActividadesAdmin(admin.ModelAdmin):
    list_display = ("objetivo_general", "objetivos_especificos", "descripcion", "estado")
    search_fields = ("descripcion",)
    list_filter = ("estado",)


class ModelFechasProyectoAdmin(admin.ModelAdmin):
    list_display = (
        "proyecto_final",
        "fecha_inicio",
        "fecha_finalizacion",
        "fecha_etapa_uno",
        "fecha_etapa_dos",
        "fecha_etapa_tres",
        "fecha_etapa_cuatro",
        "fecha_etapa_cinco",
        "fecha_etapa_seis",
    )
    search_fields = ("proyecto__nombre",)
    list_filter = ("fecha_inicio", "fecha_finalizacion")


admin.site.register(ModelFechasProyecto, ModelFechasProyectoAdmin)
