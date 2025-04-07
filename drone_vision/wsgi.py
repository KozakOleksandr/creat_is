"""
WSGI config for drone_vision project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drone_vision.settings')

application = get_wsgi_application()