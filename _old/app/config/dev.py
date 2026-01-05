from app.config.settings import *

DEBUG = True

INSTALLED_APPS.extend(["debug_toolbar"])
MIDDLEWARE.extend(["debug_toolbar.middleware.DebugToolbarMiddleware"])
