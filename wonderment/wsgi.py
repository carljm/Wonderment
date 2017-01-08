"""
WSGI config for wonderment project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""
# flake8: noqa

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wonderment.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
