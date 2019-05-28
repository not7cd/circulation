from flask import Blueprint

library = Blueprint('library', __name__, url_prefix='/libraries',
                    template_folder='templates')

from circulation.main.library import views
