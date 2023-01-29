from flask import (render_template, redirect, url_for,
                   flash)
from flask_login import login_required, current_user

from views.game import bp

@bp.route('/doctor/heal')
@login_required
def heal_player():
    flash(current_user.heal(), 'info')
    return redirect(url_for('.index'))

@bp.route("/")
@login_required
def index():
    return render_template('game/index.html')
