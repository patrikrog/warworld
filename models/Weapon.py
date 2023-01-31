from models.shared import db

class Weapon(db.Model):
    __tablename__ = 'weapon'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    min_damage = db.Column(db.Integer, nullable=False, default=1)
    max_damage = db.Column(db.Integer, nullable=False, default=1)

    level_required = db.Column(db.Integer, nullable=False, default=1)
    strength_required = db.Column(db.Integer)

    rob_chance = db.Column(db.Integer, nullable=False, default=1)
    attack_speed = db.Column(db.Integer, nullable=False, default=1)
    cost = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<Weapon {self.id}:{self.name}>'
