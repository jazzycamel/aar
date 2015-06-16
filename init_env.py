import os
from django.core.wsgi import get_wsgi_application

def init_env():
    os.environ['DJANGO_SETTINGS_MODULE']='aar_django.settings'
    return get_wsgi_application()
