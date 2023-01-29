from flask import (render_template, redirect, url_for,
                   flash)
from flask_login import login_required, current_user

from views.stats import bp

from models.User import User, Bank, UserStats


@bp.route('/increase/<string:stat_name>')
@login_required
def stat_increase(stat_name):
    match stat_name:
        case UserStats.Strength.value:
            current_user.increase_stat(UserStats.Strength, 5)
            flash('Increased strength!', 'info')
            return redirect(url_for('.index'))
        case UserStats.Psyche.value:
            current_user.increase_stat(UserStats.Psyche, 5)
            flash('Increased psyche!', 'info')
            return redirect(url_for('.index'))
        case UserStats.Vitality.value:
            current_user.increase_stat(UserStats.Vitality, 5)
            flash('Increased vitality!', 'info')
            return redirect(url_for('.index'))
        case UserStats.Agility.value:
            current_user.increase_stat(UserStats.Agility, 5)
            flash('Increased agility!', 'info')
            return redirect(url_for('.index'))


@bp.route('/reset')
@login_required
def stats_reset():
    current_user.reset_stats()
    flash('Reset stats.', 'info')
    return redirect(url_for('.index'))


@bp.route("/")
@login_required
def index():
    return render_template('stats/index.html')
