from django.contrib import admin
from .models import ModelEvaluacionAnteproyecto, ModelEvaluacionProyectoFinal

class ModelEvaluacionAnteproyectoAdmin(admin.ModelAdmin):
    list_display = ('evaluador', 'anteproyecto', 'calificacion', 'fecha_evaluacion', 'estado')
    search_fields = ('evaluador__email', 'anteproyecto__nombre')  # Ajusta según el campo correspondiente en ModelAnteproyecto
    list_filter = ('estado', 'fecha_evaluacion')
    ordering = ('-fecha_evaluacion',)
    date_hierarchy = 'fecha_evaluacion'

class ModelEvaluacionProyectoFinalAdmin(admin.ModelAdmin):
    list_display = ('jurado', 'proyecto_final', 'calificacion', 'fecha_evaluacion', 'estado')
    search_fields = ('evaluador__email', 'proyecto_final__nombre')  # Ajusta según el campo correspondiente en ModelProyectoFinal
    list_filter = ('estado', 'fecha_evaluacion')
    ordering = ('-fecha_evaluacion',)
    date_hierarchy = 'fecha_evaluacion'

admin.site.register(ModelEvaluacionAnteproyecto, ModelEvaluacionAnteproyectoAdmin)
admin.site.register(ModelEvaluacionProyectoFinal, ModelEvaluacionProyectoFinalAdmin)
