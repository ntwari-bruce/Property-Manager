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
    if request.method == "POST":
        search = request.form.get('search')
        properties = Property.query.filter(Property.location.like(f'%{search}%')).all()
        return render_template("index.html", user=current_user, properties=properties)
    else:
        properties = Property.query.all()
        return render_template("index.html", user=current_user, properties=properties)

@views.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    if request.method == 'GET':
        properties = Property.query.filter(Property.category.ilike('%buy%')).all()
        return render_template("buy.html", user=current_user, properties=properties )
    else:
        search = request.form.get('search')
        results = Property.query.filter(Property.category.like(f'%{search}%')).all()
        properties=[]
        for result in results:
            if result.category == '%buy%':
                properties.append(result)

        return redirect(url_for("views.buy", user=current_user, properties=properties))

@views.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    if request.method == 'GET':
        properties = Property.query.filter(Property.category.ilike('%rent%')).all()
        return render_template("rent.html", user=current_user, properties=properties )
    else:
        search = request.form.get('search')
        results = Property.query.filter(Property.category.like(f'%{search}%')).all()
        properties=[]
        for result in results:
            if result.category == '%rent%':
                properties.append(result)

        return redirect(url_for("views.rent", user=current_user, properties=properties))

@views.route('/favourite', methods=['GET', 'POST'])
@login_required
def favourite():
    properties = FavouriteProperty.query.all()
    return render_template("favourite.html", user=current_user, properties=properties)

@views.route('/remove_favourite/<int:id>', methods=['POST'])
@login_required
def remove_favourite(id):
    property = FavouriteProperty.query.get_or_404(id)
    db.session.delete(property)
    db.session.commit()
    return redirect(url_for('views.favourite', user=current_user))

@views.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    properties = Appointments.query.all()
    return render_template("appointment.html", user=current_user, properties=properties)


@views.route('/recall_appointment/<int:id>', methods=['POST'])
@login_required
def recall_appointment(id):
    property = Appointments.query.get_or_404(id)
    db.session.delete(property)
    db.session.commit()
    return redirect(url_for('views.appointment', user=current_user))



@views.route('/view_property/<int:id>')
@login_required
def view_property(id):
    property = Property.query.get(id)
    return render_template("view_property.html", user=current_user, property=property)

@views.route('/handleViewProperty/<int:id>', methods=['POST'])
@login_required
def handleViewProperty(id):
    action = request.form.get('action')
    property = Property.query.get(id)
    if not property:
        flash('property not found')
        return redirect(url_for('views.index'))
    
    if action == 'button_1':
        favourite = FavouriteProperty(
            user_id = current_user.id, 
            property_id = property.id,
            property_price = property.price,
            property_area = property.area, 
            property_location = property.location
        )
        # check if the property exists
        if FavouriteProperty.query.get(property.id):
            flash('Property already in favourites')
            return redirect(url_for('views.index'))
        else:
            db.session.add(favourite)
            db.session.commit()
            flash('Added to favourites')
    
    elif action == 'button_2':
        # customer's email 
        customer_email = (current_user.email)
        message = str(id)
        appointment = Appointments(
            user_id = current_user.id, 
            property_id = property.id,
            property_price = property.price,
            property_location = property.location, 
            date = func.now(),
            customer_email = current_user.email
        )
        # Check if the appointment is already booked 
        # check if the property exists
        if Appointments.query.get(property.id):
            flash('Already booked appointment for this property')
            return redirect(url_for('views.index'))
        else:
            db.session.add(appointment)
            db.session.commit()
            send_email(customer_email, message)
            flash('Appointment booked, check your email')
    else:
        flash('invalid action')
    
    return redirect(url_for('views.index'))



