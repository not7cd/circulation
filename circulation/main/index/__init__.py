from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates')

from circulation.main.index import views
