"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import os
import sys
# env config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_config.settings")
# print(sys.path)

from django.core.wsgi import get_wsgi_application
if 'SERVER_SOFTWARE' in os.environ: #BAE
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(get_wsgi_application())
else:  
    application = get_wsgi_application()