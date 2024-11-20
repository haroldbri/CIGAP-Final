from decouple import config
from dotenv import load_dotenv

from plataform_CIGAP.settings import base_dir

print(base_dir())
# load_dotenv()


env_vars = [
    "SECRET_KEY",
    "ALLOWED_HOSTS",
    "DEBUG",
    "DATABASE_URL",
    "SUPERUSER_USERNAME",
    "APP_PASSWORD",
    "SUPERUSER_PASSWORD",
]

# # print(os.getenv("SECRET_KEY"), "-----------------------")
# # print(os.getenv("DATABASE_URL"), "base de datos ")
# # print(os.getenv("ALLOWED_HOSTS"))

# for var in env_vars:
#     value = os.getenv(var)
#     print(f"{var} exists: {bool(value)}")

print(config("SECRET_KEY"))
print(config("DATABASE_URL"))
print(config("RESEND_KEY"))
