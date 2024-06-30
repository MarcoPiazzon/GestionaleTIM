from contatto import contatto_bp
from flask import Blueprint,render_template, url_for, redirect, request
from flask_login import *
from home import *
from model import *
import openpyxl
from datetime import date


@contatto_bp.route('/<int:id>/', methods=['POST', 'GET'])
def home(id):
    print("sono nwellA HOM")
    current_contatto = None

    # valore di default, indica che non sto cercando nessun utente
    if(id != 0):
        current_contatto = conn.execute(select(contatto).where(contatto.c.idContatto == id and contatto.c.idUtente == current_user.get_id())).fetchone()
    contatti = conn.execute(select(contatto).order_by(contatto.c.nome)).fetchall()
    return render_template("/contatto/contatto.html", contatti=contatti, current_contatto=current_contatto)
    

@contatto_bp.route('/getContatto', methods=['POST'])
def getContatto():
    idContatto = request.form['idSearch']
    print(idContatto)
    return home(idContatto)

@contatto_bp.route('/modifyContatto/<int:id>', methods=['POST'])
def modifyCliente(id):
    print("modifica conattto")
    nome = request.form['nome']
    secondoNome = request.form['secondoNome']
    cognome = request.form['cognome']
    viaUfficio1 = request.form['viaUfficio1'] 
    viaUfficio2 = request.form['viaUfficio2']   
    viaUfficio3 = request.form['viaUfficio3']
    provincia = request.form['provincia']
    cap = request.form['cap']
    numUfficio = request.form['numUfficio']
    numUfficio2 = request.form['numUfficio2']
    telefonoPrincipale = request.form['telefonoPrincipale']
    faxAbitazione = request.form['faxAbitazione']
    abitazione = request.form['abitazione']
    cellulare = request.form['cellulare']
    note = request.form['note']
    numeroID = request.form['numeroID']
    email1 = request.form['email1']
    email2 = request.form['email2']
    paginaWeb = request.form['paginaWeb']

    try:
        conn.execute(update(contatto).where(contatto.c.idContatto == id).values(
            nome = nome,
            idUtente = current_user.get_id(),
            secondoNome = secondoNome,
            cognome = cognome,
            viaUfficio1 = viaUfficio1,
            viaUfficio2 = viaUfficio2,
            viaUfficio3 = viaUfficio3,
            provincia = provincia,
            cap = cap,
            numUfficio = numUfficio,
            numUfficio2 = numUfficio2,
            telefonoPrincipale = telefonoPrincipale,
            faxAbitazione = faxAbitazione,
            abitazione = abitazione,
            cellulare = cellulare,
            note = note,
            numeroID = numeroID,
            email1 = email1,
            email2 = email2,
            paginaWeb = paginaWeb
        ))
        conn.commit()
        print("tutto bene")
    except Exception as error:
        print("rip")
        print(error.__cause__)


    return home(id)
    