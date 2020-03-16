from .settings import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'euphonime',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'airichan2020',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

JET_SIDE_MENU_COMPACT = True

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

LIST_PER_PAGE = 10