from flask import Blueprint

bp = Blueprint('jobs', __name__)

from views.jobs import routes
