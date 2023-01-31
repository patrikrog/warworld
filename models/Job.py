from random import randrange, random
import enum
import time

from models.shared import db
from models.Weapon import Weapon

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

    def chance(self, weapon_id):
        weapon_chance = Weapon.query.filter_by(id=weapon_id).first().rob_chance
        return 0.95 if (weapon_chance / self.difficulty) >= 1 else (weapon_chance / self.difficulty)

    def do_robbery(self, user):
        current_time = int(time.time())
        timeout = 1 if (self.timeout - user.psyche) < 1 else (self.timeout - user.psyche)

        if not current_time >= (user.last_robbery + timeout):
            return f'You still need to wait {timeout - (current_time - user.last_robbery)} seconds'
        calculated_exp = randrange(self.min_exp, self.max_exp)
        calculated_cash = randrange(self.min_cash, self.max_cash)
        calculated_damage = 0
        if random() <= 0.3:
            calculated_damage = randrange(self.min_damage, self.max_damage)
        if random() >= self.chance(user.equipped_weapon):
            return f"You failed! You don't get anything."
        else:
            user.do_job(calculated_exp, calculated_cash, calculated_damage)
            return f'You did the job! You got {calculated_exp} XP and ${calculated_cash}!'

    def __repr__(self):
        return f'<Robbery {self.id}:{self.name}'
