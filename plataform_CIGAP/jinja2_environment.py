from jinja2 import Environment
from dateutil.relativedelta import relativedelta


def environment(**options):
    env = Environment(**options)
    env.filters['add_months'] = lambda date, months: date + \
        relativedelta(months=months)  # Filtro personalizado
    return env
