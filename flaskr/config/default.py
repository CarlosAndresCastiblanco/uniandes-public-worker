from os.path import abspath, dirname, join

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Jwt Secret Key
JWT_SECRET_KEY = 'k#4ASfdfjo4343@$.-'

# Exceptions configuration
PROPAGATE_EXCEPTIONS = True

# Folder data
UPLOAD_FOLDER = './originales'

# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

AWS_ACCESS_KEY_ID = 'AKIAVI7PUQMWA7CHFW7Q'
AWS_SECRET_ACCESS_KEY = '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'