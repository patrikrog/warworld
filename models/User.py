import enum

from models.shared import db, login_manager
from flask_login import UserMixin, login_user

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
    Strength = 'strength'
    Psyche = 'psyche'
    Vitality = 'vitality'
    Agility = 'agility'

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


    level = db.Column(db.Integer, nullable=False, default=1)
    stat_points = db.Column(db.Integer, default=0)
    current_exp = db.Column(db.Integer, default=0)
    next_level = db.Column(db.Integer, nullable=False, default=50)
    cash = db.Column(db.Integer, default=0)
    bank = db.relationship('Bank', backref=db.backref('user', cascade='delete'), uselist=False)

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

    def validate_email(self, email):
        if User.query.filter_by(email=email).first():
            raise ValidationError("Email already registered!")

    def validate_username(self, username):
        if User.query.filter_by(username=username).first():
            raise ValidationError("Username already registered!")

    def heal(self):
        cost = (self.max_health - self.current_health) * COST_PER_HEALTH_POINT
        if not self.cash >= cost or not self.bank.cash >= cost:
            return (False, 0)
        self.current_health = self.max_health
        if self.cash < cost:
            self.bank.cash -= cost
        else:
            self.cash -= cost
        db.session.commit()
        return (True, cost)

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
        match stat:
            case UserStats.Strength:
                self.strength += amount
                self.stat_points -= amount
            case UserStats.Psyche:
                self.psyche += amount
                self.stat_points -= amount
            case UserStats.Vitality:
                self.vitality += amount
                if self.max_health < 1000:
                    self.max_health += amount * HEALTH_PER_POINT
                else:
                    self.max_health += amount * HEALTH_PER_POINT_DIMINISHED
                self.stat_points -= amount
            case UserStats.Agility:
                self.agility += amount
                self.stat_points -= amount
            case _:
                return
        db.session.commit()

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
