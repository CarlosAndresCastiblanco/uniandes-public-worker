from .default import *

TESTING = True
DEBUG = True

APP_ENV = APP_ENV_TESTING

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:12345678@converter.cd0qbrcafg8c.us-east-1.rds.amazonaws.com:3306/converter'