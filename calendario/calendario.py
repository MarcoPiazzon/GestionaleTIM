from calendario import calendario_bp
from flask import Blueprint,render_template, url_for, redirect, request
from flask_login import *
from home import *
from model import *
import openpyxl
from datetime import date


@calendario_bp.route('/')
def home():
    events = conn.execute(select(appuntamento)).fetchall()
    trattative = conn.execute(select(trattativa).where(trattativa.c.fase == 1)).fetchall()
    return render_template ("/calendario/calendario.html", events=events, trattative = trattative)

@calendario_bp.route('/modify', methods=['POST'])
def modifyAppuntamento():
    try:
        idapp = request.form['idapp']
        titolo = request.form['titolo']
        varieDiscussioni = request.form['varieDiscussioni']
        preventivoDaFare = request.form['preventivoDaFare']
        dataApp = request.form['dataApp']
        conn.execute(
            update(appuntamento).where(appuntamento.c.idAppuntamento==idapp).values(
                titolo = titolo,
                varieDiscussioni = varieDiscussioni,
                preventivoDaFare = preventivoDaFare,
                dataApp = dataApp,
            )
        )
        conn.commit()
        print("tutto bvene")
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()

    events = conn.execute(select(appuntamento)).fetchall()
    trattative = conn.execute(select(trattativa).where(trattativa.c.fase == 1)).fetchall()
    print(trattative)
    return render_template ("/calendario/calendario.html", events=events, trattative=trattative)

