#!/usr/bin/env python3
from app import app
from models.Job import Robbery
import models.shared as shared

app_ctx = app.app_context()
app_ctx.push()

robbery = [
    Robbery(name='Rob the kebab shop', min_exp=2, max_exp=10, min_cash=15, max_cash=30, level_required=1, min_damage=0, max_damage=3, difficulty=10, timeout=1),
    Robbery(name='Rob the gas station', min_exp=15, max_exp=30, min_cash=45, max_cash=70, level_required=15, min_damage=3, max_damage=5, difficulty=50, timeout=10),
    Robbery(name='Scam pensioners', min_exp=30, max_exp=50, min_cash=60, max_cash=110, level_required=30, min_damage=5, max_damage=10, difficulty=100, timeout=30),
    Robbery(name='Rob the supermarket', min_exp=50, max_exp=80, min_cash=110, max_cash=150, level_required=50, min_damage=10, max_damage=30, difficulty=180, timeout=100),
]

[shared.db.session.add(x) for x in robbery]
shared.db.session.commit()
