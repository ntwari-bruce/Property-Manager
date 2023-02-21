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