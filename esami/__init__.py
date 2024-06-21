from flask import Blueprint
from flask import render_template,redirect,url_for,request,make_response,abort
from model import *
esami_bp = Blueprint('esami_bp',__name__)

