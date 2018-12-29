#!/usr/bin/python
import os
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/discovering-flask/')

os.environ['APP_SETTINGS'] = 'config.DevelopmentConfig'
os.environ['DATABASE_URL'] = 'postgresql:///discover_flask_dev'

from project import app as application
application.secret_key = 'anything you wish'

