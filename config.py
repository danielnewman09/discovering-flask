# default config
import os
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '\xcd\xed\n\x82\x0e\xe4 \xf0\xc8s3S\xe7\x96\xc3\x13\x1e\xc1g\x07\xb6B\x8fu'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
