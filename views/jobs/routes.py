from flask import (request, render_template,
                   flash, redirect, url_for)
from flask_login import login_required, current_user


from views.jobs import bp
from models import shared
from models.User import User
from models.Job import Robbery

@bp.route('/do/rob/<int:job_id>')
@login_required
def do_robbery(job_id):
    robbery = Robbery.query.filter_by(id=job_id).first()
    if not robbery:
        flash("Invalid robbery id", 'error')
        return redirect(url_for('.index'))
    msg = robbery.do_robbery(user=current_user)
    flash(msg, 'info')
    return redirect(url_for('.index'))


@bp.route('/')
@login_required
def index():
    robberies = Robbery.query.all()
    return render_template('jobs/index.html', robberies=robberies)
