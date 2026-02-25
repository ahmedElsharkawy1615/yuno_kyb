"""
WSGI config for yuno_kyb project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yuno_kyb.settings')

application = get_wsgi_application()
