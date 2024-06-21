from flask import Blueprint,render_template,redirect,url_for
from model import *
from flask_login import *
admin_bp = Blueprint('admin_bp',__name__)

