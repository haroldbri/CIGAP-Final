# test_database_connection.py
import os
from django.test import TestCase
from django.db import connection
import dj_database_url


class DatabaseConnectionTest(TestCase):
    def setUp(self):
       
        self.database_url = "postgresql://cigap_ubate_user:4I175zIDOlNFrUsJjnQCmmtdmAsbqMQ9@dpg-cs5i43a3esus73avoekg-a.oregon-postgres.render.com/cigap_ubate"

    def test_database_connection(self):
        # Intenta hacer una consulta simple para verificar la conexión
        try:
            # Configurar la base de datos
            DATABASES = {
                "default": dj_database_url.parse(self.database_url, conn_max_age=600),
            }
            # Conectar a la base de datos
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
            self.assertEqual(result[0], 1)  # Debería retornar 1
        except Exception as e:
            self.fail(f"La conexión a la base de datos falló: {str(e)}")
