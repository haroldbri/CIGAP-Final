
import pytz
from datetime import datetime, timedelta
# Usamos relativedelta de dateutil
from dateutil.relativedelta import relativedelta


from datetime import datetime
from dateutil.relativedelta import relativedelta
import datetime as dt  # Asegúrate de importar datetime como dt

def fecha_culminacion_anteproyecto(fecha):
    # Verifica si la fecha es un string, un objeto datetime o un objeto date
    if isinstance(fecha, str):
        fecha_inicial = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    elif isinstance(fecha, datetime):  # Asegúrate de usar la clase datetime correcta
        fecha_inicial = fecha
    elif isinstance(fecha, dt.date):  # Cambié a dt.date
        fecha_inicial = datetime.combine(fecha, datetime.min.time())
    else:
        raise ValueError("El tipo de fecha no es válido. Debe ser un string, datetime o datetime.date.")

    # Sumar 6 meses a la fecha inicial
    fecha_final = fecha_inicial + relativedelta(months=6)

    return fecha_final


# configuracion de la Zona horaria de la aplicacion basada en la ciudad de bogota colombia
def fecha_actual():
    bogota_zone = pytz.timezone('America/Bogota')
    bogota_time = datetime.now(bogota_zone)
    bogota_timestr = bogota_time.strftime('%Y-%m-%d %H:%M:%S')
    return bogota_timestr


def fecha_maxima_respuesta(fecha):
    if not isinstance(fecha, datetime):

        fecha_inicial = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    else:
        fecha_inicial = fecha

    dias_a_sumar = 10
    dias_agregados = 0

    while dias_agregados < dias_a_sumar:
        fecha_inicial += timedelta(days=1)
        if fecha_inicial.weekday() < 5:
            dias_agregados += 1

    fecha_final = fecha_inicial
    return fecha_final

# print(fecha_actual())
