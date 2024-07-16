from flask import Blueprint,render_template,redirect,url_for
from model import *
contatto_bp = Blueprint('contatto_bp',__name__)
message = ""
