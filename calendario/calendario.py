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
    trattative = []
    try:
        #trattative = conn.execute(select(trattativa).where(trattativa.c.fase == 1)).fetchall()
        #SELECT * FROM trattativa join cliente on trattativa.idCliente = cliente.idCliente where cliente.idPortafoglio = 6
        #trattative = conn.execute(select(trattativa)).fetchall()
        
        trattative = conn.execute(select(trattativa).select_from(join(trattativa,cliente, trattativa.c.idCliente == cliente.c.idCliente)).where(cliente.c.idPortafoglio==current_user.idPort)).fetchall()
        print(trattativa)
    except Exception as error:
        print("rip")
        print(error.__cause__)
    
    return render_template ("/calendario/calendario.html", events=events, trattative = trattative)

@calendario_bp.route('/remove/<int:id>', methods=['POST'])
def removeAppuntamento(id):
    print("ok")
    try:
        print(id)
        conn.execute(delete(appuntamento).where(appuntamento.c.idAppuntamento == id))
        conn.execute(delete(trattativaappuntamento).where(trattativaappuntamento.c.idAppuntamento == id))
        conn.commit()
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()
    return redirect(url_for('calendario_bp.home'))


@calendario_bp.route('/add', methods=['POST'])
def addAppuntamento():
    try:
        print(current_user.get_id())
        print(request.form)
        idUtenteCreazione = 2 #di default, da aggiornare con l'utente corrente
        titolo = request.form['titolo']
        varieDiscussioni = request.form['varieDiscussioni']
        preventivoDaFare = request.form['preventivoDaFare']
        dataApp = request.form['dataApp']
        idTrattativa = request.form['idtrattativaAdd']
        id = conn.execute(insert(appuntamento).values(
                idUtenteCreazione = idUtenteCreazione,
                titolo = titolo,
                varieDiscussioni = varieDiscussioni,
                preventivoDaFare = preventivoDaFare,
                dataApp = dataApp,
            )
        )
        print("sto provando")
        #lastId = conn.execute(select(func.max(trattativa.c.idtrattativa))).fetchone()
        print(idTrattativa)
        print(id.inserted_primary_key[0])
        
        conn.execute(insert(trattativaappuntamento).values(
            idTrattativa = idTrattativa,
            idAppuntamento = id.inserted_primary_key[0]
        ))
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
        idTrattativa = request.form['idtrattativa']
        conn.execute(
            update(appuntamento).where(appuntamento.c.idAppuntamento==idapp).values(
                titolo = titolo,
                varieDiscussioni = varieDiscussioni,
                preventivoDaFare = preventivoDaFare,
                dataApp = dataApp,
            )
        )
        conn.execute(update(trattativaappuntamento).where(trattativaappuntamento.c.idAppuntamento == idapp).values(
            idTrattativa = idTrattativa
        ))
        conn.commit()
        print("tutto bvene")
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()

    return redirect(url_for('calendario_bp.home'))
    #return render_template ("/calendario/calendario.html", events=events, trattative=trattative)

