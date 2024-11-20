from django.test import TestCase
from .models import (
    Usuarios, ModelAnteproyecto, ModelProyectoFinal, 
    ModelAsignacionJurados, ModelObjetivoGeneral, 
    ModelObjetivosEspecificos, ModelActividades, 
    ModelFechasProyecto
)
from datetime import datetime
from django.utils import timezone



class ModelAnteproyectoTest(TestCase):
 
    def setUp(self):
        self.user = Usuarios.objects.create(
            email="anteproyecto@correo.com",
            nombres="Juan",
            apellidos="Pérez"
        )

    def test_anteproyecto_creation(self):
        anteproyecto = ModelAnteproyecto.objects.create(
            user=self.user,
            nombre_anteproyecto="Anteproyecto Ejemplo",
            nombre_integrante1="Juan Pérez",
            descripcion="Descripción del anteproyecto",
            director="Carlos Gómez",
            fecha_envio=datetime.now()
        )

        print("\n--- Datos del anteproyecto creado ---")
        print(f"Nombre del anteproyecto: {anteproyecto.nombre_anteproyecto}")
        print(f"Integrante 1: {anteproyecto.nombre_integrante1}")
        print(f"Descripción: {anteproyecto.descripcion}")
        print(f"Director: {anteproyecto.director}")
        print(f"Fecha de envío: {anteproyecto.fecha_envio}")

        self.assertIsInstance(anteproyecto, ModelAnteproyecto)
        self.assertEqual(anteproyecto.nombre_anteproyecto, "Anteproyecto Ejemplo")

class ModelProyectoFinalTest(TestCase):

    def setUp(self):
        self.user = Usuarios.objects.create(
            email="proyecto_final@correo.com",
            nombres="Ana",
            apellidos="García"
        )
        self.anteproyecto = ModelAnteproyecto.objects.create(
            user=self.user,
            nombre_anteproyecto="Anteproyecto Finalizado",
            nombre_integrante1="Ana García",
            descripcion="Descripción de anteproyecto final",
            director="Luis Rodríguez",
            fecha_envio=datetime.now()
        )

    def test_proyecto_final_creation(self):
        proyecto_final = ModelProyectoFinal.objects.create(
            user=self.user,
            anteproyecto=self.anteproyecto,
            fecha_envio=datetime.now()
        )

        print("\n--- Datos del proyecto final creado ---")
        print(f"Proyecto final asociado al anteproyecto: {proyecto_final.anteproyecto.nombre_anteproyecto}")
        print(f"Fecha de envío: {proyecto_final.fecha_envio}")

        self.assertIsInstance(proyecto_final, ModelProyectoFinal)
        self.assertEqual(proyecto_final.anteproyecto.nombre_anteproyecto, "Anteproyecto Finalizado")

class ModelAsignacionJuradosTest(TestCase):

    def setUp(self):
    
        self.user = Usuarios.objects.create(
            email="jurado@correo.com",
            nombres="Carlos",
            apellidos="Rodríguez"
        )
        self.anteproyecto = ModelAnteproyecto.objects.create(
            user=self.user,
            nombre_anteproyecto="Proyecto de Jurado",
            nombre_integrante1="Carlos Rodríguez",
            descripcion="Descripción del proyecto",
            director="María Gómez",
            fecha_envio=datetime.now()
        )
        self.proyecto_final = ModelProyectoFinal.objects.create(
            user=self.user,
            anteproyecto=self.anteproyecto,
            fecha_envio=datetime.now()
        )

    def test_asignacion_jurados_creation(self):
        jurado = ModelAsignacionJurados.objects.create(
            proyecto_final=self.proyecto_final,
            nombre_jurado="Jurado 1",
            fecha_sustentacion=datetime.now()
        )


        print("\n--- Datos del jurado asignado ---")
        print(f"Jurado: {jurado.nombre_jurado}")
        print(f"Proyecto: {jurado.proyecto_final.anteproyecto.nombre_anteproyecto}")
        print(f"Fecha de sustentación: {jurado.fecha_sustentacion}")

        self.assertIsInstance(jurado, ModelAsignacionJurados)
        self.assertEqual(jurado.nombre_jurado, "Jurado 1")

class ModelObjetivoGeneralTest(TestCase):

    def setUp(self):

        self.user = Usuarios.objects.create(
            email="objetivo_general@correo.com",
            nombres="Laura",
            apellidos="Martínez"
        )
        self.anteproyecto = ModelAnteproyecto.objects.create(
            user=self.user,
            nombre_anteproyecto="Objetivo General Proyecto",
            nombre_integrante1="Laura Martínez",
            descripcion="Descripción del proyecto",
            director="Juan Pérez",
            fecha_envio=datetime.now()
        )
        self.proyecto_final = ModelProyectoFinal.objects.create(
            user=self.user,
            anteproyecto=self.anteproyecto,
            fecha_envio=datetime.now()
        )

    def test_objetivo_general_creation(self):
        objetivo_general = ModelObjetivoGeneral.objects.create(
            proyecto_final=self.proyecto_final,
            descripcion="Objetivo General del Proyecto Final"
        )

      
        print("\n--- Datos del objetivo general creado ---")
        print(f"Objetivo General: {objetivo_general.descripcion}")
        print(f"Proyecto asociado: {objetivo_general.proyecto_final.anteproyecto.nombre_anteproyecto}")

        self.assertIsInstance(objetivo_general, ModelObjetivoGeneral)
        self.assertEqual(objetivo_general.descripcion, "Objetivo General del Proyecto Final")

class ModelObjetivosEspecificosTest(TestCase):

    def setUp(self):

        self.user = Usuarios.objects.create(
            email="objetivo_especifico@correo.com",
            nombres="Pedro",
            apellidos="Lopez"
        )
        self.anteproyecto = ModelAnteproyecto.objects.create(
            user=self.user,
            nombre_anteproyecto="Proyecto Específico",
            nombre_integrante1="Pedro Lopez",
            descripcion="Descripción del proyecto específico",
            director="Juan Pérez",
            fecha_envio=datetime.now()
        )
        self.proyecto_final = ModelProyectoFinal.objects.create(
            user=self.user,
            anteproyecto=self.anteproyecto,
            fecha_envio=datetime.now()
        )
        self.objetivo_general = ModelObjetivoGeneral.objects.create(
            proyecto_final=self.proyecto_final,
            descripcion="Objetivo General"
        )

    def test_objetivo_especifico_creation(self):
        objetivo_especifico = ModelObjetivosEspecificos.objects.create(
            objetivo_general=self.objetivo_general,
            descripcion="Objetivo Específico",
            estado=True
        )

        print("\n--- Datos del objetivo específico creado ---")
        print(f"Objetivo Específico: {objetivo_especifico.descripcion}")
        print(f"Estado: {objetivo_especifico.estado}")
        print(f"Objetivo General: {objetivo_especifico.objetivo_general.descripcion}")

        self.assertIsInstance(objetivo_especifico, ModelObjetivosEspecificos)
        self.assertEqual(objetivo_especifico.descripcion, "Objetivo Específico")


class ModelActividadesTest(TestCase):

    def setUp(self):

        self.user = Usuarios.objects.create(
            email="actividades@correo.com",
            nombres="Elena",
            apellidos="Suárez"
        )
        self.anteproyecto = ModelAnteproyecto.objects.create(
            user=self.user,
            nombre_anteproyecto="Proyecto Actividades",
            nombre_integrante1="Elena Suárez",
            descripcion="Descripción del proyecto de actividades",
            director="Juan Pérez",
            fecha_envio=datetime.now()
        )
        self.proyecto_final = ModelProyectoFinal.objects.create(
            user=self.user,
            anteproyecto=self.anteproyecto,
            fecha_envio=datetime.now()
        )
        self.objetivo_general = ModelObjetivoGeneral.objects.create(
            proyecto_final=self.proyecto_final,
            descripcion="Objetivo General del Proyecto"
        )
        self.objetivo_especifico = ModelObjetivosEspecificos.objects.create(
            objetivo_general=self.objetivo_general,
            descripcion="Objetivo Específico",
            estado=True
        )

    def test_actividad_creation(self):
        actividad = ModelActividades.objects.create(
            objetivo_general=self.objetivo_general,
            objetivos_especificos=self.objetivo_especifico,
            descripcion="Actividad de ejemplo",
            estado=True
        )

        print("\n--- Datos de la actividad creada ---")
        print(f"Descripción de la actividad: {actividad.descripcion}")
        print(f"Estado: {actividad.estado}")
        print(f"Objetivo General: {actividad.objetivo_general.descripcion}")
        print(f"Objetivo Específico: {actividad.objetivos_especificos.descripcion}")

        self.assertIsInstance(actividad, ModelActividades)
        self.assertEqual(actividad.descripcion, "Actividad de ejemplo")

class ModelFechasProyectoTest(TestCase):

    def setUp(self):

        self.user = Usuarios.objects.create(
            email="fechas@correo.com",
            nombres="Ricardo",
            apellidos="Fernández"
        )
        self.anteproyecto = ModelAnteproyecto.objects.create(
            user=self.user,
            nombre_anteproyecto="Proyecto Fechas",
            nombre_integrante1="Ricardo Fernández",
            descripcion="Descripción del proyecto de fechas",
            director="María Gómez",
            fecha_envio=datetime.now()
        )
        self.proyecto_final = ModelProyectoFinal.objects.create(
            user=self.user,
            anteproyecto=self.anteproyecto,
            fecha_envio=datetime.now()
        )

    def test_fechas_proyecto_creation(self):
        fechas_proyecto = ModelFechasProyecto.objects.create(
            proyecto_final=self.proyecto_final,
            fecha_inicio=datetime(2024, 1, 1),
            fecha_finalizacion=datetime(2024, 12, 31),
            fecha_etapa_uno=datetime(2024, 2, 1),
            fecha_etapa_dos=datetime(2024, 3, 1),
            fecha_etapa_tres=datetime(2024, 4, 1),
            fecha_etapa_cuatro=datetime(2024, 5, 1),
            fecha_etapa_cinco=datetime(2024, 6, 1),
            fecha_etapa_seis=datetime(2024, 7, 1),
            fecha_sustentacion=datetime(2024, 8, 1)
        )


        print("\n--- Datos de las fechas del proyecto ---")
        print(f"Fecha de inicio: {fechas_proyecto.fecha_inicio}")
        print(f"Fecha de finalización: {fechas_proyecto.fecha_finalizacion}")
        print(f"Fecha de etapa uno: {fechas_proyecto.fecha_etapa_uno}")
        print(f"Fecha de etapa dos: {fechas_proyecto.fecha_etapa_dos}")
        print(f"Fecha de etapa tres: {fechas_proyecto.fecha_etapa_tres}")
        print(f"Fecha de etapa cuatro: {fechas_proyecto.fecha_etapa_cuatro}")
        print(f"Fecha de etapa cinco: {fechas_proyecto.fecha_etapa_cinco}")
        print(f"Fecha de etapa seis: {fechas_proyecto.fecha_etapa_seis}")
        print(f"Fecha de sustentación: {fechas_proyecto.fecha_sustentacion}")

        self.assertIsInstance(fechas_proyecto, ModelFechasProyecto)
        self.assertEqual(fechas_proyecto.fecha_inicio, datetime(2024, 1, 1))
        self.assertEqual(fechas_proyecto.fecha_sustentacion, datetime(2024,8,1))