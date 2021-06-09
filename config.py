import os
import pwd
class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='BAD_SECRET_KEY')
    WTF_CSRF_ENABLED = True
    UPLOAD_FOLDER=os.path.join(os.getenv("HOME"), "vep_data")
    ALLOWED_EXTENSIONS = {'vcf','vcf.gz'}
    VEP_PATH='/opt/vep/.vep'


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True