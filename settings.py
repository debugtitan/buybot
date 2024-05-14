from __future__ import absolute_import

from pathlib import Path
import environ
BASE_DIR = Path(__file__).resolve(strict=True).parent

env = environ.Env()
environ.Env.read_env(str(BASE_DIR /  ".env"), overwrite=True)


# Telegram Bot Token
TOKEN = env.str("TOKEN", None)

# Bot Username ---- without @ e.g solpingbot
BOT_USERNAME = env.str("BOT_USERNAME","solpingbot")

# Secret Key
SECRET_KEY = env.str("DJANGO_SECRET_KEY",default="***")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG_MODE",False)

# SUPER ADMIN: first admin bot responds to when started forthe first time
SUPER_ADMIN = env.int("TELEGRAM_ADMIN_ID",1185692914)

INSTALLED_APPS = [
    "pingbot.resources"
]



# Database
if env.bool("USE_DJANGO_IN_MEMORY_DATABASE",False):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'pingbot.sqlite3',
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": env.str("POSTGRESQL_ENGINE", "django.db.backends.postgresql_psycopg2"),
            "NAME": env.str("POSTGRESQL_NAME", "***"),
            "USER": env.str("POSTGRESQL_USER", "***"),
            "PASSWORD": env.str("POSTGRESQL_PASSWORD", "***"),
            "HOST": env.str("POSTGRESQL_HOST","***"),
            "PORT": env.int("POSTGRESQL_PORT", 5432),
        },
    }

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Blockchain
PRIVATE_RPC_CLIENT = env.str("RPC_CLIENT")


# Django Solo
GET_SOLO_TEMPLATE_TAG_NAME = 'get_config'