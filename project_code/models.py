from .database import db
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func
from datetime import datetime


class Property(db.Model):
    """Model representing a property listing in the application."""
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
    """Model representing a registered user in the application."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    property = db.relationship('Property', backref='user')


class PasswordResetToken(db.Model):
    """Model representing a password reset token for a user."""
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), unique=True, nullable=False)
    data = db.Column(db.PickleType, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def is_expired(self):
          """Check if the password reset token is expired."""
          return datetime.utcnow() > self.data['expires_at']

# favourite properties
class FavouriteProperty(db.Model):
    """Model representing a user's favourite properties"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    property_type = db.Column(db.String(10000), db.ForeignKey('property.type'))
    property_price = db.Column(db.String(10000), db.ForeignKey('property.price'))
    property_area = db.Column(db.String(10000), db.ForeignKey('property.area'))
    property_location = db.Column(db.String(10000), db.ForeignKey('property.location'))

# appointments
class Appointments(db.Model):
    """Model representing a user's booked appointment."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    property_price = db.Column(db.String(10000), db.ForeignKey('property.price'))
    property_location = db.Column(db.String(10000), db.ForeignKey('property.location'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    customer_email = db.Column(db.String(10000), db.ForeignKey('user.email'))






   
