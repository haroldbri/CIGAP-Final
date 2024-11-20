import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataform_CIGAP.settings')
django.setup()

from django.contrib.auth.models import Group

grupos = ['Estudiantes', 'Correspondencia', 'Directores']

for nombre in grupos:
    grupo, creado = Group.objects.get_or_create(name=nombre)
    if creado:
        print(f'Grupo "{nombre}" creado.')
    else:
        print(f'Grupo "{nombre}" ya existe.')
