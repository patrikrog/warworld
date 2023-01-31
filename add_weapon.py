#!/usr/bin/env python3
from app import app
from models.Weapon import Weapon
import models.shared as shared

app_ctx = app.app_context()
app_ctx.push()

weapon = [
    Weapon(name='Fists', min_damage=1, max_damage=4, level_required=1, strength_required=0, rob_chance=10, attack_speed=4, cost=0),
    Weapon(name='Kitchen knife', min_damage=5, max_damage=10, level_required=15, strength_required=25, rob_chance=50, attack_speed=6, cost=1500),
]

[shared.db.session.add(x) for x in weapon]
shared.db.session.commit()
