from flask import Flask, request, url_for, redirect
from flask_admin.base import BaseView
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from .database import db
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView


# Name of the database file
DB_NAME = "database.db"


def create_app():
    """
    Create a new Flask application and return it.

    Returns:
        Flask: the Flask application
    """
    app = Flask(__name__)

    # Set the secret key used for session management
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    # Set the URI for the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Automatically reload templates when they are modified
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Initialize the database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Create a Flask-Admin instance
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')

    # Register blueprints for the views and authentication
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import the database models
    from .models import User, Property, Appointments

    # Initialize the Flask-Login extension for user authentication
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Define the function for loading a user from the database based on their ID
    @login_manager.user_loader
    def load_user(id):
        try:
            return User.query.get(int(id))
        except (TypeError, ValueError):
            return None

    # Create a view for adding a new property
    class AddPropertyView(BaseView):
        column_filters = ['location']

        @expose('/', methods=['GET','POST'])
        def index(self):
            if request.method == 'POST':
                new_property = Property(
                    type=request.form.get('type'),
                    category=request.form.get('category'),
                    area=request.form.get('area'),
                    address=request.form.get('address'),
                    developer=request.form.get('developer'),
                    location=request.form.get('location'),
                    price=request.form.get('price'),
                    bedroom=request.form.get('bedroom'),
                    bathroom=request.form.get('bathroom'),
                    furnished=request.form.get('furnished'),
                    date=request.form.get('date'),
                    user=current_user,
                    cctv=request.form.get('cctv'),
                    parking=request.form.get('parking'),
                    image_1=request.form.get('image1'),
                    image_2=request.form.get('image2'),
                    image_3=request.form.get('image3'),
                    image_4=request.form.get('image4')
                )

                db.session.add(new_property)
                db.session.commit()

                return redirect(url_for('admin.index'))

            return self.render('admin/add_property2.html')

    # Create a custom model view for displaying database records with the primary key displayed
    class CustomModelView(ModelView):
        column_display_pk = True # to show the primary key in the list view
        column_hide_backrefs = True

    # Filters to the property view
    class PropertyModelView(ModelView):
            column_filters =  ('location','developer','price','category')
    
    # Create a custom model view for the user model
    class UserView(CustomModelView):
            column_list = ('id', 'email', 'password')
    
    # Create a custom model view for the user's booked appointment
    class appointmentView(CustomModelView):
         column_list = ('id', 'customer_email','user_id', 'property_id', 'property_price', 'property_location', 'date')
        
    
         
    # Add models to the Flask-Admin interface
    admin.add_view(UserView(User, db.session))
    admin.add_view(PropertyModelView(Property, db.session))
    admin.add_view(AddPropertyView(name='Add Property'))
    admin.add_view(appointmentView(Appointments, db.session))
    
    
    
    return app

# Ensure the database file exists before the application runs
def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

