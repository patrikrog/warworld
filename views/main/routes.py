from flask import render_template, redirect, url_for
from flask_login import current_user

from views.main import bp
from views.auth import forms

from models.User import User


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('game.index'))
    form = forms.LoginForm()
    return render_template('main/index.html', form=form)
