from flask import (render_template, redirect, url_for,
                   flash)
from flask_login import login_required, current_user

from views.game import bp

@bp.route('/doctor/heal')
@login_required
def heal_player():
    status, cost = current_user.heal()
    if status:
        flash(f'You healed yourself! It cost you ${cost}.', 'info')
    else:
        flash(f"You couldn't afford to pay the doctor bills!", 'warning')

    return redirect(url_for('.index'))

@bp.route("/")
@login_required
def index():
    return render_template('game/index.html')
