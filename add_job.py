#!/usr/bin/env python3
from flask import current_app
from app import create_app
from app.models.Job import Robbery
import app.models.shared as shared

app = create_app()
app_ctx = app.app_context()
app_ctx.push()

robbery = []

job.append(Robbery(name='Rob the kebab shop', min_exp=2, max_exp=10, min_cash=15, max_cash=30, level_required=1))
job.append(Robbery(name='Rob the gas station', min_exp=15, max_exp=30, min_cash=45, max_cash=70, level_required=15))
job.append(Robbery(name='Scam pensioners', min_exp=30, max_exp=50, min_cash=60, max_cash=110, level_required=30))
job.append(Robbery(name='Rob the supermarket', min_exp=50, max_exp=80, min_cash=110, max_cash=150, level_required=50))

[shared.db.session.add(x) for x in job]
shared.db.session.commit()

grow = []
grow.append(Grow(name='Brew wine', min_exp=50, max_exp=80, min_cash=110, max_cash=150, level_required=50))

[shared.db.session.add(x) for x in grow]
shared.db.session.commit()
