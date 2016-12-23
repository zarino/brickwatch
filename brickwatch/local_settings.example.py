# Copy this file to local_settings.py
# and customise the variables below.

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'database.sqlite'),
    }
}

# Docs: https://github.com/timotheus/ebaysdk-python
EBAY_APP_ID = '###'
EBAY_DEV_ID = '###'
EBAY_CERT_ID = '###'
EBAY_TOKEN = '######'

# Docs: http://brickset.com/tools/webservices/v2
BRICKSET_API_KEY = '###'
BRICKSET_USER_HASH = '###'
