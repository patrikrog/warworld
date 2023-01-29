from flask import (request, render_template,
                   flash, redirect, url_for)
from flask_login import login_required, current_user


from views.jobs import bp
from models import shared
from models.User import User
from models.Job import Robbery

@bp.route('/do/rob/<id>')
@login_required
def do_robbery(id):
    robbery = Robbery.query.filter_by(id=id).first()
    if not robbery:
        flash("Invalid robbery id", 'error')
        return redirect(url_for('.index'))
    exp, cash = robbery.do_robbery(user=current_user)
    flash(f'You did the job! You got {exp} XP and ${cash}!', 'info')
    return redirect(url_for('.index'))


@bp.route('/')
@login_required
def index():
    robberies = Robbery.query.all()
    return render_template('jobs/index.html', robberies=robberies)
