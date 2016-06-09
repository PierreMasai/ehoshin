from .base import *

DEBUG = True

# SSL security
os.environ['HTTPS'] = "on"
os.environ['wsgi.url_scheme'] = 'https'
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# To complete
DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "",
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "",
        }
}
