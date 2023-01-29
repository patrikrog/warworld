from flask import Blueprint

bp = Blueprint('dev', __name__)

from views.dev import routes
