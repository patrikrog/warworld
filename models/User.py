import enum
import time

from models.shared import db, login_manager
from flask_login import UserMixin, login_user, logout_user
from models.Weapon import Weapon

EXP_INCREASE_PER_LEVEL=5
MAX_EXP_CAP=1000
STAT_POINTS_PER_LEVEL=5
HEALTH_PER_POINT=5
HEALTH_PER_POINT_DIMINISHED=2
COST_PER_HEALTH_POINT=5

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserStats(enum.Enum):
    Strength = 'Muscle'
    Psyche = 'Smarts'
    Vitality = 'Stamina'
    Agility = 'Swiftness'

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    # Basic account information.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    online = db.Column(db.Boolean, default=False)

    # Account stats, health, money etc.
    max_health = db.Column(db.Integer, nullable=False, default=100)
    current_health = db.Column(db.Integer, default=100)
    dead = db.Column(db.Boolean, default=False)

    strength = db.Column(db.Integer,default=0)
    psyche = db.Column(db.Integer, default=0)
    agility = db.Column(db.Integer, default=0)
    vitality = db.Column(db.Integer, default=0)

    equipped_weapon = db.Column(db.Integer, db.ForeignKey('weapon.id'), default=1)

    last_robbery = db.Column(db.Integer, nullable=False, default=int(time.time()))

    level = db.Column(db.Integer, nullable=False, default=1)
    stat_points = db.Column(db.Integer, default=0)
    current_exp = db.Column(db.Integer, default=0)
    next_level = db.Column(db.Integer, nullable=False, default=50)
    cash = db.Column(db.Integer, default=0)
    bank = db.relationship('Bank', backref=db.backref('user', cascade='delete'), uselist=False)

    def buy_weapon(self, weapon_id):
        weapon = Weapon.query.filter_by(id=weapon_id).first()
        if not weapon:
            return "That weapon doesn't exist."
        if self.cash < weapon.cost:
            return "You don't have enough money to buy that."
        if self.strength < weapon.strength_required:
            return f"You don't have enough {UserStats.Strength.value} to hold that weapon, weakling."
        if self.equipped_weapon == weapon_id:
            return f"You already have this weapon equipped."

        self.equipped_weapon = weapon_id
        self.cash -= weapon.cost
        db.session.commit()
        return f'You bought {weapon.name} for ${weapon.cost}!'

    def check_dead(self):
        if not self.current_health <= 0:
            return False
        self.dead = True
        return True

    def login(self, remember_me):
        self.online = True
        login_user(self, remember=remember_me)
        db.session.commit()

    def logout(self):
        self.online = False
        logout_user()
        db.session.commit()

    def validate_email(self, email):
        if User.query.filter_by(email=email).first():
            raise ValidationError("Email already registered!")

    def validate_username(self, username):
        if User.query.filter_by(username=username).first():
            raise ValidationError("Username already registered!")

    def heal(self):
        cost = (self.max_health - self.current_health) * COST_PER_HEALTH_POINT

        if self.cash <= cost:
            return "You can't afford healing."
        if self.current_health >= self.max_health:
            return "You don't seem to be needing a doctor right now."
        self.current_health = self.max_health

        self.cash -= cost

        if self.dead:
            self.dead = False
        db.session.commit()
        return f'You healed yourself! It cost you ${cost}.'

    def damage(self, amount):
        self.current_health -= amount
        self.check_dead()
        db.session.commit()

    def create_bank(self):
        if Bank.query.filter_by(id=self.id).first():
            raise ValidationError('Bank already exists?')
        newbank = Bank(cash=0, user_id=self.id)
        self.bank = newbank

    def do_job(self, experience, cash, damage):
        self.current_exp += experience
        self.cash += cash
        self.damage(damage)
        if self.current_exp >= self.next_level:
            remainder = self.current_exp - self.next_level
            if self.next_level < MAX_EXP_CAP:
                self.next_level += EXP_INCREASE_PER_LEVEL
            self.level += 1
            self.current_exp = remainder
            self.stat_points += STAT_POINTS_PER_LEVEL
        self.last_robbery = int(time.time())
        db.session.commit()

    def reset_stats(self):
        self.strength = 0
        self.vitality = 0
        self.psyche = 0
        self.agility = 0
        self.stat_points = (self.level - 1) * STAT_POINTS_PER_LEVEL
        self.max_health = 100
        self.current_health = self.max_health
        db.session.commit()

    def increase_stat(self, stat, amount):
        # We don't want users adding stat points they don't have.
        if self.stat_points <= 0:
            msg = "You don't have enough stat points."
            return msg

        match stat:
            case UserStats.Strength:
                self.strength += amount
                self.stat_points -= amount
                msg = f"Increased {UserStats.Strength.value}."

            case UserStats.Psyche:
                self.psyche += amount
                self.stat_points -= amount
                msg = f"Increased {UserStats.Psyche.value}."

            case UserStats.Vitality:
                self.vitality += amount
                if self.max_health < 1000:
                    self.max_health += amount * HEALTH_PER_POINT
                else:
                    self.max_health += amount * HEALTH_PER_POINT_DIMINISHED
                self.stat_points -= amount
                msg = f"Increased {UserStats.Vitality.value}."

            case UserStats.Agility:
                self.agility += amount
                self.stat_points -= amount
                msg = f"Increased {UserStats.Agility.value}."

        db.session.commit()
        return msg

    def __repr__(self):
        return f'<User {self.username}>'

class Bank(db.Model):
    __tablename__ = 'bank'

    id = db.Column(db.Integer, primary_key=True)
    cash = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def deposit(self, user, amount):
       self.cash += amount
       user.cash -= amount
       db.session.commit()

    def withdraw(self, user, amount):
       self.cash -= amount
       user.cash += amount
       db.session.commit()

    def __repr__(self):
        return f'<Bank {self.id}>'
