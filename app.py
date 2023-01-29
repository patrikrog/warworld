from flask import Flask, flash
from flask_login import login_required, current_user
from flask_migrate import Migrate


from config import Config

import models.shared as shared
from models.User import User

app = Flask('Warworld')
app.config.from_object(Config)

shared.db.init_app(app)
shared.migrate.init_app(app, shared.db)
shared.login_manager.init_app(app)
shared.bcrypt.init_app(app)

from views.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from views.dev import bp as dev_bp
app.register_blueprint(dev_bp, url_prefix="/dev")

from views.game import bp as game_bp
app.register_blueprint(game_bp, url_prefix="/city")

from views.stats import bp as stats_bp
app.register_blueprint(stats_bp, url_prefix="/profile/stats")

from views.bank import bp as bank_bp
app.register_blueprint(bank_bp, url_prefix="/city/bank")

from views.jobs import bp as jobs_bp
app.register_blueprint(jobs_bp, url_prefix="/jobs")

from views.main import bp as main_bp
app.register_blueprint(main_bp)


@app.before_request
def check_dead():
    if current_user.is_anonymous and not current_user.is_authenticated:
        return

    if current_user.check_dead():
        flash(f'You are dead! You should go to a doctor and get that checked out...', 'warning')
