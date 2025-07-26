"""
WSGI config for Code_Acadmy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application




# add your project path
path = '"D:\Django_projects\Code_Acadmy"'
if path not in sys.path:
    sys.path.insert(0, path)

# set your Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Code_Acadmy.settings')

# import Django WSGI application
application = get_wsgi_application()
