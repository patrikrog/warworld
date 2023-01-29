from flask import Blueprint

bp = Blueprint('game', __name__)

from views.game import routes
