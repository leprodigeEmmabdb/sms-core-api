import socket

from settings.base import *

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_EXPOSE_HEADERS = [
    "Content-Disposition",
]

# DB_HOST = "db_postgres"

DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# IF MIGRATION FAILED WITH ERROR 1071
# ALTER DATABASE utulivu_db CHARACTER SET utf8 COLLATE utf8_general_ci;

ASGI_APPLICATION = "root.asgi.application"

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# DEFAULT_FROM_EMAIL = "admin@utulivurdc.com"
# EMAIL_HOST = "pesasango.com"
# EMAIL_HOST_USER = "info@pesasango.com"
# EMAIL_HOST_PASSWORD = ">^=0]_U5(W7>1Zj%[Y-63g"
# EMAIL_PORT = 587


hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "general.log"),
            "formatter": "verbose",
        },
        "errorfile": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "error.log"),
            "when": "midnight",  # daily, you can use 'midnight' as well
            "interval": 1,
            # 'backupCount': 100,  # 100 days backup
            "formatter": "verbose",
        },
        "debugfile": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "daily.log"),
            "when": "midnight",  # daily, you can use 'midnight' as well
            "interval": 1,
            # 'backupCount': 100,  # 100 days backup
            "formatter": "verbose",
        },
    },
    "loggers": {
        # "app_store":{
        # "app_store.views":{
        "": {
            "handlers": ["errorfile", "debugfile"],
            # "level": "ERROR"
        },
        "___": {
            "handlers": [
                "console",
            ],
            "level": "DEBUG",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} ({levelname}) - {lineno} - {name} - {message}",
            # log_format = '%(levelname)s %(asctime)s %(module)s:%(funcName)s line:%(lineno)d %(message)s'
            "style": "{",
        }
    },
}
