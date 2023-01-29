from flask import Blueprint

bp = Blueprint('stats', __name__)

from views.stats import routes
