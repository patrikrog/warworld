from flask import render_template
from flask_login import login_required, current_user

from views.dev import bp
from models.User import User, Bank

@login_required
@bp.route("/users")
def users():
    query = User.query.all()
    users = []
    for user in query:
        bank = Bank.query.filter_by(id=user.bank.id).first()
        users.append({
            "username": user.username,
            "email": user.email,
            'online': user.online,
            "level": user.level,
            "current_xp": user.current_exp,
            "next_level": user.next_level,
            "cash": user.cash,
            "bank": bank.cash,
            'health': {'current_health': user.current_health, 'max_health': user.max_health, 'dead': user.dead},
            "stats": {'strength': user.strength, 'psyche': user.psyche, 'vitality': user.vitality, 'agility': user.agility},
            "password": user.password.decode(encoding="utf-8")
        })
    return users
