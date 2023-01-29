from flask import Blueprint

bp = Blueprint('bank', __name__)

from views.bank import routes
