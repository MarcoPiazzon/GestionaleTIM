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

@calendario_bp.route('/remove/<int:id>', methods=['POST'])
def removeAppuntamento(id):
    print("ok")
    try:
        print(id)
        conn.execute(delete(appuntamento).where(appuntamento.c.idAppuntamento == id))
        conn.commit()
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()
    return redirect(url_for('calendario_bp.home'))


@calendario_bp.route('/add', methods=['POST'])
def addAppuntamento():
    try:
        print(current_user.get_id)
        idUtenteCreazione = 2 #di default, da aggiornare con l'utente corrente
        idapp = request.form['idapp']
        titolo = request.form['titolo']
        varieDiscussioni = request.form['varieDiscussioni']
        preventivoDaFare = request.form['preventivoDaFare']
        dataApp = request.form['dataApp']
        conn.execute(insert(appuntamento).values(
                idUtenteCreazione = idUtenteCreazione,
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
    
    return redirect(url_for('calendario_bp.home'))

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

    return redirect(url_for('calendario_bp.home'))
    #return render_template ("/calendario/calendario.html", events=events, trattative=trattative)

