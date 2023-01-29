from random import randrange, random
import enum

from models.shared import db

class Robbery(db.Model):
    __tablename__ = 'robbery'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    min_exp = db.Column(db.Integer, default=0)
    max_exp = db.Column(db.Integer, default=0)
    min_cash = db.Column(db.Integer, default=0)
    max_cash = db.Column(db.Integer, default=0)
    min_damage = db.Column(db.Integer, default=0)
    max_damage = db.Column(db.Integer, default=0)
    level_required = db.Column(db.Integer, default=0)
    difficulty = db.Column(db.Integer, default=0)
    timeout = db.Column(db.Integer, nullable=False, default=1)


    def do_robbery(self, user):
        calculated_exp = randrange(self.min_exp, self.max_exp)
        calculated_cash = randrange(self.min_cash, self.max_cash)
        calculated_damage = 0
        if random() <= 0.3:
            calculated_damage = randrange(self.min_damage, self.max_damage)
        user.do_job(calculated_exp, calculated_cash, calculated_damage)
        return (calculated_exp, calculated_cash)

    def __repr__(self):
        return f'<Robbery {self.id}:{self.name}'
