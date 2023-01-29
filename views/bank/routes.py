from flask import (render_template, redirect, url_for,
                   flash)
from flask_login import login_required, current_user

from views.bank import bp
from models.User import Bank

@bp.route("/withdraw")
@login_required
def bank_withdraw():
    bank = Bank.query.filter_by(user_id=current_user.id).first()
    bank.withdraw(current_user, current_user.bank.cash)
    return redirect(url_for('.index'))

@bp.route("/deposit")
@login_required
def bank_deposit():
    bank = Bank.query.filter_by(user_id=current_user.id).first()
    bank.deposit(current_user, current_user.cash)
    return redirect(url_for('.index'))

@bp.route("/")
@login_required
def index():
    return render_template('game/index.html')
