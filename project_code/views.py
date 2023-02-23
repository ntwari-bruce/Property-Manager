from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Property
from . import db 
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html",user=current_user)

@views.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    return render_template("buy.html", user=current_user)

@views.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    return render_template("rent.html", user=current_user)

@views.route('/favourite', methods=['GET', 'POST'])
@login_required
def favoutire():
    return render_template("favourite.html", user=current_user)

@views.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    return render_template("appointment.html", user=current_user)

@views.route('/view_property', methods=['GET', 'POST'])
@login_required
def view_property():
    return render_template("view_property.html", user=current_user)
