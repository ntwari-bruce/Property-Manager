from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Property, FavouriteProperty, Appointments, User
from sqlalchemy.sql import func
from .database import db 
from .helpers import send_email


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """User's home page"""
    if request.method == "POST":
        search = request.form.get('search')
        # Search by location
        properties = Property.query.filter(Property.location.like(f'%{search}%')).all()
        return render_template("index.html", user=current_user, properties=properties)
    else:
        properties = Property.query.all()
        return render_template("index.html", user=current_user, properties=properties)


@views.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    """The view for properties for sale only"""
    if request.method == 'GET':
        properties = Property.query.filter(Property.category.ilike('%buy%')).all()
        return render_template("buy.html", user=current_user, properties=properties )
    else:
        search = request.form.get('search')
        # Search property by location
        results = Property.query.filter(Property.category.like(f'%{search}%')).all()
        properties=[]
        for result in results:
            if result.category == '%buy%':
                properties.append(result)

        return redirect(url_for("views.buy", user=current_user, properties=properties))
    

@views.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    """The view for properties for rent only"""
    if request.method == 'GET':
        properties = Property.query.filter(Property.category.ilike('%rent%')).all()
        return render_template("rent.html", user=current_user, properties=properties )
    else:
        search = request.form.get('search')
        # Search by location
        results = Property.query.filter(Property.category.like(f'%{search}%')).all()
        properties=[]
        for result in results:
            if result.category == '%rent%':
                properties.append(result)

        return redirect(url_for("views.rent", user=current_user, properties=properties))
    

@views.route('/favourite', methods=['GET', 'POST'])
@login_required
def favourite():
    """The view for favourite Properties"""
    properties = FavouriteProperty.query.all()
    return render_template("favourite.html", user=current_user, properties=properties)


@views.route('/remove_favourite/<int:id>', methods=['POST'])
@login_required
def remove_favourite(id):
    """Remove/delete a property from favourite properies"""
    property = FavouriteProperty.query.filter_by(user_id=current_user.id, property_id=id).first()
    db.session.delete(property)
    db.session.commit()
    return redirect(url_for('views.favourite', user=current_user))


@views.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    """The view for the user's booked appointment"""
    properties = Appointments.query.all()
    return render_template("appointment.html", user=current_user, properties=properties)


@views.route('/recall_appointment/<int:id>', methods=['POST'])
@login_required
def recall_appointment(id):
    """Recall booked appointment"""
    property = Appointments.query.filter_by(user_id=current_user.id, property_id=id).first()
    db.session.delete(property)
    db.session.commit()
    return redirect(url_for('views.appointment', user=current_user))


@views.route('/view_property/<int:id>')
@login_required
def view_property(id):
    """View Property's details"""
    property = Property.query.get(id)
    return render_template("view_property.html", user=current_user, property=property)


@views.route('/handleViewProperty/<int:id>', methods=['POST'])
@login_required
def handleViewProperty(id):
    """Add property to favourites on book the visit appointment"""
    action = request.form.get('action')
    property = Property.query.get(id)
    if not property:
        flash('property not found', category='error')
        return redirect(url_for('views.index'))
    
    # Adding property to favourites
    if action == 'button_1':
        # check if the property exists
        if FavouriteProperty.query.filter_by(user_id=current_user.id, property_id=property.id).first():
            flash('Property already in favourites', category='error')
            return redirect(request.referrer)
        else:
            favourite = FavouriteProperty(
                user_id = current_user.id, 
                property_id = property.id,
                property_price = property.price,
                property_area = property.area, 
                property_location = property.location
        )
        
        
            db.session.add(favourite)
            db.session.commit()
            flash('Added to favourites')
            return redirect(request.referrer)
        
    # Booking the appointment to visit the property
    elif action == 'button_2':
        # Check if the appointment is already booked 
        if Appointments.query.filter_by(user_id=current_user.id, property_id=property.id).first():
            flash('Already booked appointment for this property', category='error')
            return redirect(request.referrer)
        else:

            # customer's email 
            customer_email = (current_user.email)
            message = f'Id "{str(id)}" located in {property.location}-{property.address}'
            appointment = Appointments(
            user_id = current_user.id, 
            property_id = property.id,
            property_price = property.price,
            property_location = property.location, 
            date = func.now(),
            customer_email = current_user.email

        )
            db.session.add(appointment)
            db.session.commit()
            send_email(customer_email, message)
            flash('Appointment booked, check your email')
    else:
        flash('invalid action')
    
    return redirect(request.referrer)



