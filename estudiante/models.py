from django.db import models
from django import forms
import base64
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from login.models import Usuarios


class ModelAnteproyecto(models.Model):

    user = models.ForeignKey(
        Usuarios,
        on_delete=models.CASCADE,
        related_name="Anteproyecto",
        blank=True,
        null=True,
    )
    nombre_anteproyecto = models.CharField(max_length=200)
    nombre_integrante1 = models.CharField(max_length=50)
    nombre_integrante2 = models.CharField(
        max_length=50, null=True, blank=True
    )  # Cambio aquí
    descripcion = models.TextField(
        max_length=5000, null=True, blank=True
    )  # Cambio aquí
    carta_presentacion = models.BinaryField(null=True, blank=True)
    anteproyecto = models.BinaryField(null=True, blank=True)
    director = models.CharField(max_length=50, null=True)
    codirector = models.CharField(max_length=50, null=True, blank=True)  # Cambio aquí
    fecha_envio = models.DateTimeField(null=True, blank=True)
    documento_radicado = models.BinaryField(null=True, blank=True)
    # estas son modificadas por correspondencia
    solicitud_enviada = models.BooleanField(null=True, blank=True)
    estado = models.BooleanField(default=False)
    documento_radicado = models.BinaryField(null=True, blank=True)
    documento_concepto = models.BinaryField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Anteproyectos"


class ModelProyectoFinal(models.Model):
    user = models.OneToOneField(
        Usuarios,
        on_delete=models.CASCADE,
        related_name="Proyecto_Final",
        blank=True,
        null=True,
    )
    anteproyecto = models.OneToOneField(
        ModelAnteproyecto,
        on_delete=models.CASCADE,
        related_name="Proyecto_Final",
        blank=True,
        null=True,
    )
    proyecto_final = models.BinaryField(null=True, blank=True)
    carta_presentacion_final = models.BinaryField(null=True, blank=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    solicitud_enviada = models.BooleanField(default=False, null=True, blank=True)
    estado = models.BooleanField(default=False, null=True, blank=True)
    documento_radicado = models.BinaryField(null=True, blank=True)
    documento_concepto = models.BinaryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(ModelProyectoFinal, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Proyectos Finales"


class ModelAsignacionJurados(models.Model):
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal,
        on_delete=models.CASCADE,
        related_name="Jurados",
        blank=True,
        null=True,
    )
    nombre_jurado = models.CharField(max_length=50)
    fecha_sustentacion = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Jurados Asignados"


class ModelObjetivoGeneral(models.Model):
    proyecto_final = models.OneToOneField(
        ModelProyectoFinal,
        on_delete=models.CASCADE,
        related_name="objetivo_general",
        blank=True,
        null=True,
    )
    descripcion = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Objetivos Generales"


class ModelObjetivosEspecificos(models.Model):
    objetivo_general = models.ForeignKey(
        ModelObjetivoGeneral,
        on_delete=models.CASCADE,
        related_name="objetivos_especificos",
        blank=True,
        null=True,
    )
    descripcion = models.CharField(max_length=1000, blank=True, null=True)
    observaciones = models.CharField(max_length=1000, blank=True, null=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    fecha_observacion = models.DateTimeField(blank=True, null=True)
    documento_avance = models.BinaryField(blank=True, null=True)
    documento_correcciones = models.BinaryField(blank=True, null=True)
    estado = models.BooleanField(blank=True, default=False)

    class Meta:
        verbose_name_plural = "Objetivos especificos"


class ModelActividades(models.Model):
    objetivo_general = models.ForeignKey(
        ModelObjetivoGeneral,
        on_delete=models.CASCADE,
        related_name="actividades",
        blank=True,
        null=True,
    )
    objetivos_especificos = models.ForeignKey(
        ModelObjetivosEspecificos,
        on_delete=models.CASCADE,
        related_name="actividades",
        blank=True,
        null=True,
    )
    descripcion = models.CharField(max_length=1000, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Actividades"


class ModelFechasProyecto(models.Model):
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, related_name="fechas", on_delete=models.CASCADE
    )
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_finalizacion = models.DateTimeField(blank=True, null=True)
    fecha_etapa_uno = models.DateField(blank=True, null=True)
    fecha_etapa_dos = models.DateField(blank=True, null=True)
    fecha_etapa_tres = models.DateField(blank=True, null=True)
    fecha_etapa_cuatro = models.DateField(blank=True, null=True)
    fecha_etapa_cinco = models.DateField(blank=True, null=True)
    fecha_etapa_seis = models.DateField(blank=True, null=True)
    fecha_sustentacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Fechas del proyecto {self.proyecto_final.anteproyecto.nombre_anteproyecto}"

    class Meta:
        verbose_name_plural = "Fechas de proyectos"
