"""
WSGI config for SchoolManagement project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
# django imports
from django.core.wsgi import get_wsgi_application

# inter app imports
from setting_configs import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv("SETTINGS"))

application = get_wsgi_application()
