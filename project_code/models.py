from .database import db
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10000))
    category = db.Column(db.String(10000))
    area = db.Column(db.String(10000))
    address = db.Column(db.String(10000))
    developer = db.Column(db.String(10000))
    location = db.Column(db.String(10000))
    price = db.Column(db.String(10000))
    bedroom = db.Column(db.String(10000))
    bathroom = db.Column(db.String(10000))
    furnished = db.Column(db.String(10000))
    cctv = db.Column(db.String(100))
    parking = db.Column(db.String(100))
    image_1 = db.Column(db.String(10000))
    image_2 = db.Column(db.String(10000))
    image_3 = db.Column(db.String(10000))
    image_4 = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    property = db.relationship('Property', backref='user')

favourites = db.Table('favourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('property_id', db.Integer, db.ForeignKey('property.id'))
)

# favourite properties
class FavouriteProperty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    property_price = db.Column(db.String(10000), db.ForeignKey('property.price'))
    property_type = db.Column(db.String(10000), db.ForeignKey('property.type'))
    property_area = db.Column(db.String(10000), db.ForeignKey('property.area'))
    property_location = db.Column(db.String(10000), db.ForeignKey('property.location'))

# appointments
class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    property_price = db.Column(db.String(10000), db.ForeignKey('property.price'))
    property_location = db.Column(db.String(10000), db.ForeignKey('property.location'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    customer_email = db.Column(db.String(10000), db.ForeignKey('user.email'))





   
