from flask import Blueprint

book = Blueprint('book', __name__, url_prefix='/books',
                 template_folder='templates')

from circulation.main.book import views
