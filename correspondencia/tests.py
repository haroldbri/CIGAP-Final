from django.test import TestCase
from login.models import Usuarios
from estudiante.models import ModelAnteproyecto, ModelProyectoFinal, ModelFechasProyecto
from correspondencia.models import (
    ModelRetroalimentaciones,
    ModelInformacionEntregaFinal,
    ModelSolicitudes,
    ModelDocumentos,
    ModelFechasComite,
)
from datetime import datetime, datetime


 
class ModelRetroalimentacionesTest(TestCase):
    def setUp(self):
        self.user = Usuarios.objects.create(
            email="evaluador@test.com",
            nombres="Nombre Evaluador",
            apellidos="Apellido Evaluador",
        )
        self.anteproyecto = ModelAnteproyecto.objects.create(
            user=self.user,
            nombre_anteproyecto="Eduardo",
            nombre_integrante1="Rafael",
            nombre_integrante2="Duvan",
            descripcion="Descripción de prueba",
            carta_presentacion=b"",
            anteproyecto=b"",  
            director="Manuel",
            codirector="Alex",
            fecha_envio=datetime.now(), 
            solicitud_enviada=True,
            estado=True,
            documento_radicado=b"",  
            documento_concepto=b"", 
        )
        self.retroalimentacion = ModelRetroalimentaciones.objects.create(
            anteproyecto=self.anteproyecto,
            user=self.user,
            retroalimentacion="Retroalimentación de prueba",
            fecha_retroalimentacion=datetime.now(),
            estado="Aprobado",
            revs_dadas=5,
        )

    def test_retroalimentacion_creation(self):
        self.assertIsNotNone(self.retroalimentacion)
        self.assertEqual(self.retroalimentacion.estado, "Aprobado")
        print(f"Retroalimentación creada con éxito: {self.retroalimentacion}")

        print(f"Retroalimentación creada con éxito: {self.retroalimentacion}")
        print(
            f"ID Retroalimentación: {self.retroalimentacion.id}, Estado: {self.retroalimentacion.estado}"
        )

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(ModelRetroalimentaciones._meta.verbose_name_plural),
            "Retroalimentaciones",
        )
        verbose_name_plural = ModelRetroalimentaciones._meta.verbose_name_plural
        print(f"Verbose Name Plural: {verbose_name_plural}")
        self.assertEqual(verbose_name_plural, "Retroalimentaciones")


class ModelInformacionEntregaFinalTest(TestCase):
    def setUp(self):
        self.user = Usuarios.objects.create(
            email="evaluador@test.com",
            nombres="Nombre Evaluador",
            apellidos="Apellido Evaluador",
        )
        self.anteproyecto = ModelAnteproyecto.objects.create(
            user=self.user,
            nombre_anteproyecto="Eduardo",
            nombre_integrante1="Rafael",
            nombre_integrante2="Duvan",
            descripcion="Descripción de prueba",
            carta_presentacion=b"",
            anteproyecto=b"",
            director="Manuel",
            codirector="Alex",
            fecha_envio=datetime.now(),
            solicitud_enviada=True,
            estado=True,
            documento_radicado=b"",
            documento_concepto=b"",
        )
        self.proyecto_final = ModelProyectoFinal.objects.create(
            proyecto_final=b"",
            carta_presentacion_final=b"",
            fecha_envio=datetime.now(),
            solicitud_enviada=True,
            estado=True,
            documento_radicado=b"",
            documento_concepto=b"",
        )
        self.fechas_proyecto = ModelFechasProyecto.objects.create(
            proyecto_final=self.proyecto_final,
            fecha_inicio="2024-01-7",
            fecha_finalizacion="2024-01-7",
            fecha_etapa_uno="2024-01-7",
            fecha_etapa_dos="2024-01-7",
            fecha_etapa_tres="2024-01-7",
            fecha_etapa_cuatro="2024-01-7",
            fecha_etapa_cinco="2024-01-7",
            fecha_etapa_seis="2024-01-7",
            fecha_sustentacion="2024-01-7",
        )
        self.entrega_final = ModelInformacionEntregaFinal.objects.create(
            anteproyecto=self.anteproyecto,
            proyecto_final=self.proyecto_final,
            fechas_proyecto=self.fechas_proyecto,
            fecha_finalizacion=datetime.now(),
        )

    def test_informacion_entrega_final_creation(self):
        self.assertIsNotNone(self.entrega_final)
        self.assertEqual(self.entrega_final.anteproyecto, self.anteproyecto)
        print(f"Información de Entrega Final creada con éxito: {self.entrega_final}")

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(ModelInformacionEntregaFinal._meta.verbose_name_plural),
            "Informaciones de Entregas Finales",
        )
        verbose_name_plural = ModelInformacionEntregaFinal._meta.verbose_name_plural
        print(f"Verbose Name Plural: {verbose_name_plural}")
        self.assertEqual(verbose_name_plural, "Informaciones de Entregas Finales")


class ModelSolicitudesTest(TestCase):
    def setUp(self):
        self.user = Usuarios.objects.create(
            email="evaluador@test.com",
            nombres="Nombre Evaluador",
            apellidos="Apellido Evaluador",
        )
        self.anteproyecto = ModelAnteproyecto.objects.create(
            user=self.user,
            nombre_anteproyecto="Eduardo",
            nombre_integrante1="Rafael",
            nombre_integrante2="Duvan",
            descripcion="Descripción de prueba",
            carta_presentacion=b"",
            anteproyecto=b"",
            director="Manuel",
            codirector="Alex",
            fecha_envio=datetime.now(),
            solicitud_enviada=True,
            estado=True,
            documento_radicado=b"",
            documento_concepto=b"",
        )
        self.solicitud = ModelSolicitudes.objects.create(
            user=self.user,
            anteproyecto=self.anteproyecto,
            tipo_solicitud="cambio_nombre",
            motivo_solicitud="Motivo de prueba",
            fecha_envio=datetime.now(),
            estado=True,
        )

    def test_solicitud_creation(self):
        self.assertIsNotNone(self.solicitud)
        self.assertEqual(self.solicitud.tipo_solicitud, "cambio_nombre")
        print(f"Solicitud creada con éxito: {self.solicitud}")

    def test_verbose_name_plural(self):
        self.assertEqual(str(ModelSolicitudes._meta.verbose_name_plural), "Solicitudes")
        verbose_name_plural = ModelSolicitudes._meta.verbose_name_plural
        print(f"Verbose Name Plural: {verbose_name_plural}")
        self.assertEqual(verbose_name_plural, "Solicitudes")


class ModelDocumentosTest(TestCase):
    def setUp(self):
        self.documento = ModelDocumentos.objects.create(
            nombre_documento="Documento Prueba",
            version="v1.0",
            descripcion="Descripción de prueba",
            fecha_cargue=datetime.now(),
        )

    def test_documento_creation(self):
        self.assertIsNotNone(self.documento)
        self.assertEqual(self.documento.nombre_documento, "Documento Prueba")
        print(f"Documento creado con éxito: {self.documento}")

    def test_verbose_name_plural(self):
        self.assertEqual(str(ModelDocumentos._meta.verbose_name_plural), "Documentos")
        verbose_name_plural = ModelDocumentos._meta.verbose_name_plural
        print(f"Verbose Name Plural: {verbose_name_plural}")
        self.assertEqual(verbose_name_plural, "Documentos")


class ModelFechasComiteTest(TestCase):
    def setUp(self):
        self.fechas_comite = ModelFechasComite.objects.create(
            ano_actual=2024,
            periodo_academico="2024-1",
            primer_encuentro="2024-01-15",
            segundo_encuentro="2024-02-15",
        )

    def test_fechas_comite_creation(self):
        self.assertIsNotNone(self.fechas_comite)
        self.assertEqual(self.fechas_comite.ano_actual, 2024)
        print(f"Fechas de Comité creadas con éxito: {self.fechas_comite}")

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(ModelFechasComite._meta.verbose_name_plural), "Fechas de Comite"
        )
        verbose_name_plural = str(ModelFechasComite._meta.verbose_name_plural)
        print(f"Verbose Name Plural: {verbose_name_plural}")
        
