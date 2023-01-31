from flask import (request, render_template,
                   flash, redirect, url_for)
from flask_login import current_user, login_required

from views.auth import bp, forms
from models import shared
from models.User import User

@bp.route('/logout')
@login_required
def logout():
    current_user.logout()
    return redirect(url_for('main.index'))


@bp.route('/login')
def login():
    return redirect(url_for("main.index"))

@bp.route('/login', methods=["POST"])
def login_post():
    form = forms.LoginForm()

    if not form.validate_on_submit():
        flash("Error with form.", "error")
        return redirect(url_for("auth.login"))

    username = form.username.data
    password = shared.bcrypt.generate_password_hash(form.password.data)

    user = User.query.filter(User.username.ilike(username)).first()

    if not user or shared.bcrypt.check_password_hash(user.password, password):
        flash("Username or password incorrect", "error")
        return redirect(url_for("auth.login"))

    user.login(form.remember_me.data)
    return redirect(url_for("game.index"))

@bp.route('/register', methods=['POST', 'GET'])
def register():
    form = forms.RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = shared.bcrypt.generate_password_hash(form.password.data)

        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash(f"Username or email already registered", "error")
            return redirect(url_for("auth.register"))

        newuser = User(username=username, email=email, password=password)
        newuser.create_bank()

        shared.db.session.add(newuser)
        shared.db.session.commit()
        flash(f"Account successfully created!", "success")
        return redirect(url_for("main.index"))

    return render_template("auth/register.html", form=form)
