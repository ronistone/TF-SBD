import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TESTING = True
CSRF_ENABLED = True
SECRET_KEY = 'this-really-needs-to-be-changed'
DB_HOST='localhost'
DB_NAME='agencia'
DB_USER='postgres'
DB_PASSWORD='1234'
DB_PORT='5432'