from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10000))
    area = db.Column(db.Integer)
    address = db.Column(db.String(10000))
    landmark = db.Column(db.String(10000))
    delevoler = db.Column(db.String(10000))
    location = db.Column(db.String(10000))
    price = db.Column(db.Integer)
    bedroom = db.Column(db.String(10000))
    bathroom = db.Column(db.String(10000))
    furnished = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    property = db.relationship('Property')
