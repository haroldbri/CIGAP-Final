from django.test import TestCase
from .models import Usuarios, ModelError
from datetime import datetime


class UsuariosModelTest(TestCase):
    def test_usuario_creation(self):
        usuario = Usuarios.objects.create(
            email="testuser@correo.com",
            nombres="Juan",
            apellidos="Pérez"
        )
 

        print("\n--- Datos de usuario creado en test_usuario_creation ---")
        print(f"Email: {usuario.email}")
        print(f"Nombres: {usuario.nombres}")
        print(f"Apellidos: {usuario.apellidos}")
        print(f"Nombre completo: {usuario.nombre_completo}")
        

        self.assertIsInstance(usuario, Usuarios)
        self.assertEqual(usuario.email, "testuser@correo.com")
        self.assertEqual(usuario.nombres, "Juan")
        self.assertEqual(usuario.apellidos, "Pérez")
        self.assertEqual(usuario.nombre_completo, "Juan Pérez")  

    def test_usuario_creation_with_image_and_token(self):
        usuario = Usuarios.objects.create(
            email="otro_usuario@correo.com",
            nombres="Ana",
            apellidos="García",
            imagen=b"imagen_bytes",
            token="abcd1234token"
        )


class ModelErrorTest(TestCase):
    def setUp(self):
        self.user = Usuarios.objects.create(
            email="usuario_error@correo.com",
            nombres="Error",
            apellidos="Usuario"
        )

    def test_model_error_creation(self):
        error = ModelError.objects.create(
            user=self.user,
            ruta_origen="/path/to/source",
            estado=500,
            fecha_hora_error=datetime.now()
        )

        print("\n--- Datos del registro de error creado en test_model_error_creation ---")
        print(f"Usuario: {error.user.email}")
        print(f"Ruta de origen: {error.ruta_origen}")
        print(f"Estado: {error.estado}")
        print(f"Fecha y hora del error: {error.fecha_hora_error}")

        self.assertIsInstance(error, ModelError)
        self.assertEqual(error.user, self.user)
        self.assertEqual(error.ruta_origen, "/path/to/source")
        self.assertEqual(error.estado, 500)
        self.assertIsNotNone(error.fecha_hora_error)

    def test_model_error_nullable_fields(self):
        error = ModelError.objects.create(
            estado=404,
            fecha_hora_error=datetime.now()
        )

        print("\n--- Datos del registro de error creado en test_model_error_nullable_fields ---")
        print(f"Usuario: {error.user}")
        print(f"Ruta de origen: {error.ruta_origen}")
        print(f"Estado: {error.estado}")
        print(f"Fecha y hora del error: {error.fecha_hora_error}")

        self.assertIsInstance(error, ModelError)
        self.assertIsNone(error.user)
        self.assertIsNone(error.ruta_origen)
        self.assertEqual(error.estado, 404)
        self.assertIsNotNone(error.fecha_hora_error)

        self.assertIsInstance(Usuarios, Usuarios)
        self.assertEqual(Usuarios.email, "otro_usuario@correo.com")
        self.assertEqual(Usuarios.imagen, b"imagen_bytes")
        self.assertEqual(Usuarios.token, "abcd1234token")
        self.assertEqual(Usuarios.nombre_completo, "Ana García")

    def test_usuario_roles(self):
        usuario = Usuarios.objects.create(
            email="director@correo.com",
            nombres="Carlos",
            apellidos="Rodriguez"
        )
        usuario.rol = "director"
        usuario.save()

        print("\n--- Datos de usuario creado en test_usuario_roles ---")
        print(f"Email: {usuario.email}")
        print(f"Nombres: {usuario.nombres}")
        print(f"Apellidos: {usuario.apellidos}")
        print(f"Rol: {usuario.rol}")

        self.assertEqual(usuario.rol, "director")


class ModelErrorTest(TestCase):
    def setUp(self):
        self.user = Usuarios.objects.create(
            email="usuario_error@correo.com",
            nombres="Error",
            apellidos="Usuario"
        )

    def test_model_error_creation(self):
        error = ModelError.objects.create(
            user=self.user,
            ruta_origen="/path/to/source",
            estado=500,
            fecha_hora_error=datetime.now()
        )

        print("\n--- Datos del registro de error creado en test_model_error_creation ---")
        print(f"Usuario: {error.user.email}")
        print(f"Ruta de origen: {error.ruta_origen}")
        print(f"Estado: {error.estado}")
        print(f"Fecha y hora del error: {error.fecha_hora_error}")

        self.assertIsInstance(error, ModelError)
        self.assertEqual(error.user, self.user)
        self.assertEqual(error.ruta_origen, "/path/to/source")
        self.assertEqual(error.estado, 500)
        self.assertIsNotNone(error.fecha_hora_error)

    def test_model_error_nullable_fields(self):

        error = ModelError.objects.create(
            estado=404,
            fecha_hora_error=datetime.now()
        )

        print("\n--- Datos del registro de error creado en test_model_error_nullable_fields ---")
        print(f"Usuario: {error.user}")
        print(f"Ruta de origen: {error.ruta_origen}")
        print(f"Estado: {error.estado}")
        print(f"Fecha y hora del error: {error.fecha_hora_error}")

        self.assertIsInstance(error, ModelError)
        self.assertIsNone(error.user)
        self.assertIsNone(error.ruta_origen)
        self.assertEqual(error.estado, 404)
        self.assertIsNotNone(error.fecha_hora_error)

    def setUp(self):
        self.user = Usuarios.objects.create(
            email="usuario_error@correo.com",
            nombres="Error",
            apellidos="Usuario"
        )

    def test_model_error_creation(self):
        error = ModelError.objects.create(
            user=self.user,
            ruta_origen="/path/to/source",
            estado=500,
            fecha_hora_error=datetime.now()
        )

        print("\n--- Datos del registro de error creado en test_model_error_creation ---")
        print(f"Usuario: {error.user.email}")
        print(f"Ruta de origen: {error.ruta_origen}")
        print(f"Estado: {error.estado}")
        print(f"Fecha y hora del error: {error.fecha_hora_error}")

        self.assertIsInstance(error, ModelError)
        self.assertEqual(error.user, self.user)
        self.assertEqual(error.ruta_origen, "/path/to/source")
        self.assertEqual(error.estado, 500)
        self.assertIsNotNone(error.fecha_hora_error)

    def test_model_error_nullable_fields(self):
        error = ModelError.objects.create(
            estado=404,
            fecha_hora_error=datetime.now()
        )

        print("\n--- Datos del registro de error creado en test_model_error_nullable_fields ---")
        print(f"Usuario: {error.user}")
        print(f"Ruta de origen: {error.ruta_origen}")
        print(f"Estado: {error.estado}")
        print(f"Fecha y hora del error: {error.fecha_hora_error}")

        self.assertIsInstance(error, ModelError)
        self.assertIsNone(error.user)
        self.assertIsNone(error.ruta_origen)
        self.assertEqual(error.estado, 404)
        self.assertIsNotNone(error.fecha_hora_error)