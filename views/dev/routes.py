from flask import render_template
from flask_login import login_required, current_user

from views.dev import bp
from models.User import User, Bank
from models.Weapon import Weapon

@login_required
@bp.route('/users')
def users():
    query = User.query.all()
    users = []
    for user in query:
        bank = Bank.query.filter_by(id=user.bank.id).first()
        users.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password.decode(encoding='utf-8'),
            'online': user.online,
            'health': {'current_health': user.current_health, 'max_health': user.max_health, 'dead': user.dead},
            'stats': {'stat_points': user.stat_points, 'strength': user.strength, 'psyche': user.psyche, 'vitality': user.vitality, 'agility': user.agility},
            'equipped_weapon': Weapon.query.filter_by(id=user.equipped_weapon).first().name,
            'last_robbery': user.last_robbery,
            'level': user.level,
            'current_xp': user.current_exp,
            'next_level': user.next_level,
            'cash': user.cash,
            'bank': bank.cash,
        })
    return users
