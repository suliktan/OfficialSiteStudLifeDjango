"""
WSGI config for Students Life project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'students_life.settings')

application = get_wsgi_application()
