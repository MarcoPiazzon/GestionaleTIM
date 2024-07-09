from flask import Blueprint,render_template, url_for, redirect, request, Response
from trattativa import *
from flask_login import *
from model import *
from login.login import bcrypt
import openpyxl
from datetime import date

@trattativa_bp.route('/<int:id>', methods=['GET', 'POST'])
def home(id):
    trattative = conn.execute(select(trattativa).select_from(join(cliente, trattativa, cliente.c.idCliente == trattativa.c.idCliente)).where(cliente.c.idUtente == current_user.get_id() and cliente.c.idPortafoglio == id)).fetchall()
    print(trattative)
    return render_template ("/trattativa/trattativa.html",trattative = trattative)
