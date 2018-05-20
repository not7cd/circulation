import os
import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask.ext.pagedown import PageDown
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager(app)
bootstrap = Bootstrap(app)
pagedown = PageDown(app)
avatars = UploadSet('avatars', IMAGES)
configure_uploads(app, avatars)

from circulation.main import main, auth, user, book, comment, library, log
from circulation.api import api_bp

for blueprint in [main, auth, user, book, comment, library, log, api_bp]:
    app.register_blueprint(blueprint)

from circulation import models

exists_db = os.path.isfile(app.config['DB_PATH'])
if not exists_db:
    logger.warning('no db found under ', app.config['DB_PATH'])
    from . import db_fill
