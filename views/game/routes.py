from flask import (render_template, redirect, url_for,
                   flash)
from flask_login import login_required, current_user

from views.game import bp

from models.Weapon import Weapon
from models.User import User

@bp.route('/online')
@login_required
def online_players():
    online_players = User.query.filter_by(online=True).all()
    return render_template('game/online.html', online_players=online_players)

@bp.route('/doctor/heal')
@login_required
def heal_player():
    flash(current_user.heal(), 'info')
    return redirect(url_for('.index'))

@bp.route("/")
@login_required
def index():
    return render_template('game/index.html')

@bp.route('/shop/weapons')
@login_required
def weapon_shop():
    weapons = Weapon.query.all()
    return render_template('game/shop/weapons.html', weapons=weapons)

@bp.route('/shop/weapons/buy/<int:weapon_id>')
@login_required
def buy_weapon(weapon_id):
    msg = current_user.buy_weapon(weapon_id)
    flash(msg, 'info')
    return redirect(url_for('game.weapon_shop'))
