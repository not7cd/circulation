from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates')
from circulation.main.auth import views
