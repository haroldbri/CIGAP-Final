import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Establecer el entorno de configuración de Django antes de cualquier importación de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plataform_CIGAP.settings")

import django

django.setup()

# Importar el modelo de usuario personalizado
from login.models import Usuarios

# Obtener variables de entorno para el superusuario
print(os.environ.get("PASSWORD"))
nombres = os.getenv("SUPERUSER_NOMBRES")
apellidos = os.getenv("SUPERUSER_APELLIDOS")
email = os.getenv("SUPERUSER_EMAIL")
password = os.getenv("PASSWORD")

# Imprimir email y contraseña
print(f"Email: {email}")
print(f"Password: {password}")

# Crear el superusuario si no existe
if not Usuarios.objects.filter(email=email).exists():
    Usuarios.objects.create_superuser(
        email=email, nombres=nombres, apellidos=apellidos, password=password
    )
    print(f'Superusuario "{email}" creado con éxito.')
else:
    print(f'El superusuario "{email}" ya existe.')
