from django.test import TestCase
from login.models import Usuarios
from estudiante.models import ModelAnteproyecto, ModelProyectoFinal
from director.models import ModelEvaluacionAnteproyecto, ModelEvaluacionProyectoFinal
from datetime import datetime
from django.utils import timezone

class ModelEvaluacionAnteproyectoTest(TestCase):
    def setUp(self):
        self.evaluador = Usuarios.objects.create(
            email="evaluador@test.com",
            nombres="Nombre Evaluador",
            apellidos="Apellido Evaluador",
        )

        self.anteproyecto = ModelAnteproyecto.objects.create(
            nombre_anteproyecto="Anteproyecto Prueba",
            descripcion="Descripción de prueba"
        )
        
         
        
        self.evaluacion_anteproyecto = ModelEvaluacionAnteproyecto.objects.create(
            evaluador=self.evaluador,
            anteproyecto=self.anteproyecto,
            calificacion=4.5,
            comentarios="Comentarios de prueba",
            fecha_evaluacion=timezone.now(), 
            fecha_asignacion=timezone.now(),  
            estado=True
        )

    def test_evaluacion_anteproyecto_creation(self):
        self.assertIsNotNone(self.evaluacion_anteproyecto)
        self.assertEqual(self.evaluacion_anteproyecto.evaluador, self.evaluador)
        self.assertEqual(self.evaluacion_anteproyecto.calificacion, 4.5)
        self.assertEqual(self.evaluacion_anteproyecto.comentarios, "Comentarios de prueba")
        print(f"Evaluación de Anteproyecto creada con éxito: {self.evaluacion_anteproyecto}")

    def test_verbose_name_plural(self):
        self.assertEqual(str(ModelEvaluacionAnteproyecto._meta.verbose_name_plural), "Evaluaciones de Anteproyectos")
        print(f"Prueba Evaluación de Anteproyecto: Nombre plural es '{ModelEvaluacionAnteproyecto._meta.verbose_name_plural}'")
        verbose_name_plural = str(ModelEvaluacionAnteproyecto._meta.verbose_name_plural)
        print(f"Prueba Evaluación de Anteproyecto: Nombre plural es '{verbose_name_plural}'")
        self.assertEqual(verbose_name_plural, "Evaluaciones de Anteproyectos")


class ModelEvaluacionProyectoFinalTest(TestCase):
    def setUp(self):
        self.jurado = Usuarios.objects.create(
            email="jurado@test.com",
            nombres="Nombre Jurado",
            apellidos="Apellido Jurado",
        )

       
        self.anteproyecto = ModelAnteproyecto.objects.create(
            user=self.jurado,
            nombre_anteproyecto="Eduardo",
            nombre_integrante1="Rafael",
            nombre_integrante2="Duvan",
            descripcion="Descripción de prueba",
            carta_presentacion=b"", 
            anteproyecto=b"",  
            director="Manuel",
            codirector="Alex",
            fecha_envio=timezone.now(),  
            solicitud_enviada=True,
            estado=True,
            documento_radicado=b"", 
            documento_concepto=b"" 
        )
        
      
        self.proyecto_final = ModelProyectoFinal.objects.create(
            anteproyecto=self.anteproyecto,
            proyecto_final=b"",
            carta_presentacion_final=b"",  
            fecha_envio=timezone.now(),  
            solicitud_enviada=True,
            estado=True,
            documento_radicado=b"",  
            documento_concepto=b""  
        )


        self.evaluacion_proyecto = ModelEvaluacionProyectoFinal.objects.create(
            jurado=self.jurado,
            proyecto_final=self.proyecto_final,
            calificacion=4.8,
            comentarios="Comentarios para el proyecto final",
            fecha_evaluacion=timezone.now(), 
            fecha_asignacion=timezone.now(), 
            estado=True
        )

    def test_evaluacion_proyecto_creation(self):
        self.assertIsNotNone(self.evaluacion_proyecto)
        self.assertEqual(self.evaluacion_proyecto.calificacion, 4.8)
        self.assertEqual(self.evaluacion_proyecto.comentarios, "Comentarios para el proyecto final")
        print(f"Evaluación de Proyecto Final creada con éxito: {self.evaluacion_proyecto}")

    def test_verbose_name_plural(self):
        self.assertEqual(str(ModelEvaluacionProyectoFinal._meta.verbose_name_plural), "Evaluaciones de Proyectos Finales")
        print(f"Prueba Evaluación de Proyecto Final: Nombre plural es '{ModelEvaluacionProyectoFinal._meta.verbose_name_plural}'")
        verbose_name_plural = str(ModelEvaluacionProyectoFinal._meta.verbose_name_plural)
        print(f"Prueba Evaluación de Proyecto Final: Nombre plural es '{verbose_name_plural}'")
       