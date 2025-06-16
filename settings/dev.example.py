import socket


from settings.base import *

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_EXPOSE_HEADERS = [
    "Content-Disposition",
]

DB_HOST = "127.0.0.1"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB'),
        'USER': os.environ.get('DB_USER'),
        "PASSWORD": os.environ.get('DB_PWD'),
        "HOST": DB_HOST,
        "PORT": os.environ.get('DB_PORT'),
        "TIME_ZONE": TIME_ZONE,
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 600
    },
}

# IF MIGRATION FAILED WITH ERROR 1071
# ALTER DATABASE utulivu_db CHARACTER SET utf8 COLLATE utf8_general_ci;

ASGI_APPLICATION = 'root.asgi.application'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = DB_HOST
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'from@obidano.com'

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
