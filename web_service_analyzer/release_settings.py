import os
from .settings import BASE_DIR

DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ALLOWED_HOSTS = ['188.225.76.126', '372902-cg66680.tmweb.ru']