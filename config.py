import os

basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.environ.get('DB_PATH', os.path.join(basedir, 'circulation.db'))

MAX_CONTENT_LENGTH = 1024 * 1024

UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'upload/')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_PATH

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.environ['SECRET_KEY']

FLASKY_ADMIN = 'root@gmail.com'
