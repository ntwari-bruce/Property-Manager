from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import email_validator
from datetime import datetime, timedelta
import uuid

from .database import db
from .models import User, PasswordResetToken
from .helpers import send_email, send_email_password


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Allows user to log in to the application.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user with the provided email exists
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # Log in the user
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect email or password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    # Render the login template
    return render_template("user_login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
    Logs out the current user.
    """
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user"""
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password')
        password2 = request.form.get('password_confirmation')

        try:
            # Validate the email address using the email-validator library
            email_validator.validate_email(email)
        except email_validator.EmailNotValidError as e:
            flash(str(e), category='error')
            return redirect(url_for('auth.register'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.index'))

    return render_template("user_register.html", user=current_user)


@auth.route('/forgot_password', methods=['GET','POST'])
def forgot_password():
    """Handle the forgot password request"""
    if request.method == "POST":
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a token that includes the user's email and timestamps
            token = str(uuid.uuid4())
            now = datetime.utcnow()
            expires_at = now + timedelta(hours=24)
            token_data = {'email': email, 'expires_at': expires_at}
            db.session.add(PasswordResetToken(token=token, data=token_data))
            db.session.commit()
            # Send the password reset link to the user's email
            reset_link = url_for('auth.reset_password', token=token, _external=True)
            message = f'Click the link below to reset your password:\n\n{reset_link}'
            send_email_password(recipient_email=email, message=message)

            flash('Password reset link has been sent to your email address', category='success')
        else:
            flash('Email does not exist.', category='error')

    return render_template('forgot_password.html', user=current_user)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset Password route"""
    
    # Get the PasswordResetToken object associated with the token
    token_obj = PasswordResetToken.query.filter_by(token=token).first()

    # If no token found, redirect to forgot password page with error message
    if not token_obj:
        flash('Invalid or expired password reset link.', category='error')
        return redirect(url_for('auth.forgot_password'))

    # If token has expired, delete it and redirect to forgot password page with error message
    if token_obj.is_expired:
        flash('The password reset link has expired.', category='error')
        db.session.delete(token_obj)
        db.session.commit()
        return redirect(url_for('auth.forgot_password'))

    # If request method is POST, process the form
    if request.method == 'POST':
        # Get the passwords from the form
        password1 = request.form.get('password')
        password2 = request.form.get('password_confirmation')

        # If passwords don't match, show error message
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        # If password is too short, show error message
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Update the user's password in the database and delete the token
            user = User.query.filter_by(email=token_obj.data['email']).first()
            user.password = generate_password_hash(password1, method='sha256')
            db.session.delete(token_obj)
            db.session.commit()
            # Log the user in and show success message
            login_user(user, remember=True)
            flash('Password has been reset!', category='success')
            return redirect(url_for('views.index'))

    # If request method is GET, show the reset password form
    return render_template('reset_password.html', user=current_user, token=token)


