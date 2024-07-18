from calendario import calendario_bp
from flask import Blueprint,render_template, url_for, redirect, request
from flask_login import *
from home import *
from model import *
import openpyxl
from datetime import date

titolo = "Calendario"

@calendario_bp.route('/')
def home():
    #events = conn.execute(select(appuntamento, utente.c.nome, utente.c.cognome).select_from(join(appuntamento, utente, appuntamento.c.idUtenteCreazione == utente.c.idUtente))).fetchall()
    events = conn.execute(
        select(appuntamento, utente.c.nome, utente.c.cognome, trattativa.c.idtrattativa, trattativa.c.nomeopportunita).select_from(
            join(utente, outerjoin(appuntamento, 
                 outerjoin(trattativa, trattativaappuntamento, trattativa.c.idtrattativa == trattativaappuntamento.c.idtrattativa), appuntamento.c.idappuntamento == trattativaappuntamento.c.idappuntamento),utente.c.idutente == appuntamento.c.idutentecreazione
            )
        )
        ).fetchall()
    print(events)
    trattative = []
    try:
        #trattative = conn.execute(select(trattativa).where(trattativa.c.fase == 1)).fetchall()
        #SELECT * FROM trattativa join cliente on trattativa.idCliente = cliente.idCliente where cliente.idPortafoglio = 6
        #trattative = conn.execute(select(trattativa)).fetchall()
        
        trattative = conn.execute(select(trattativa).select_from(join(trattativa,cliente, trattativa.c.idcliente == cliente.c.idcliente)).where(cliente.c.idportafoglio==current_user.idPort)).fetchall()
        
        print(trattativa)
    except Exception as error:
        conn.rollback()
        print("rip")
        print(error.__cause__)
    
    print(titolo)
    print("rend cale")
    return render_template ("/calendario/calendario.html", events=events, trattative = trattative, titolo = titolo)

@calendario_bp.route('/remove/<int:id>', methods=['POST'])
def removeAppuntamento(id):
    print("ok")
    try:
        print(id)
        conn.execute(delete(appuntamento).where(appuntamento.c.idappuntamento == id))
        conn.execute(delete(trattativaappuntamento).where(trattativaappuntamento.c.idappuntamento == id))
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
        idUtenteCreazione = current_user.get_id() #di default, da aggiornare con l'utente corrente
        titolo = request.form['titolo']
        varieDiscussioni = request.form['varieDiscussioni']
        preventivoDaFare = request.form['preventivoDaFare']
        dataApp = request.form['dataApp']
        idTrattativa = request.form['idtrattativaAdd']

        id = conn.execute(insert(appuntamento).values(
                idutentecreazione = idUtenteCreazione,
                titolo = titolo,
                variediscussioni = varieDiscussioni,
                preventivodafare = preventivoDaFare,
                dataapp = dataApp,
            )
        )
        print("sto provando")
        #lastId = conn.execute(select(func.max(trattativa.c.idtrattativa))).fetchone()
        print(idTrattativa)
        print(id.inserted_primary_key[0])
        
        conn.execute(insert(trattativaappuntamento).values(
            idtrattativa = idTrattativa,
            idappuntamento = id.inserted_primary_key[0]
        ))
        print("tutto bvene")
        global message 
        message = "Appuntamento aggiunto"
    except Exception as error:
        print("rip")
        print(error)
        print(error.__cause__)
        conn.rollback()
    
    return redirect(url_for('calendario_bp.home'))

def checkDate(val):
    if(isinstance(val, str)):
        if val == '':
            return None
        else: 
            return val 

def checkNull(val):
    print(type(val))
    if val == '':
        return 0
    else: 
        return val


@calendario_bp.route('/modify', methods=['POST'])
def modifyAppuntamento():
    try:
        idapp = request.form['idapp']
        titolo = request.form['titolo']
        variediscussioni = request.form['varieDiscussioni']
        preventivodafare = request.form['preventivoDaFare']
        dataapp = checkDate(request.form['dataApp'])
        idtrattativa = checkNull(request.form['idtrattativa'])
        conn.execute(
            update(appuntamento).where(appuntamento.c.idappuntamento==idapp).values(
                titolo = titolo,
                variediscussioni = variediscussioni,
                preventivodafare = preventivodafare,
                dataapp = dataapp,
            )
        )
        conn.execute(update(trattativaappuntamento).where(trattativaappuntamento.c.idappuntamento == idapp).values(
            idtrattativa = idtrattativa
        ))
        print("tutto bvene")
        global message
        message = "Appuntamento modificato"
    except Exception as error:
        print("rip")
        print(error)
        print(error.__cause__)
        conn.rollback()

    return redirect(url_for('calendario_bp.home'))
    #return render_template ("/calendario/calendario.html", events=events, trattative=trattative)

