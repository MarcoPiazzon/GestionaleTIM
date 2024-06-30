from flask import Blueprint,render_template, url_for, redirect, request
from home import *
from flask_login import *
from model import *
from login.login import bcrypt
import openpyxl
from datetime import date

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    contatti = conn.execute(select(contatto)).fetchall()
    
    #corsilaurea_all = conn.execute(select(corsilaurea)).fetchall()
    contattiUtente = conn.execute(select(contatto)).fetchall()
    """conn.execute(insert(utente).values(
        nome = 'Marco',
        cognome= 'Piazzon',
        email= 'mp@gmail.com',
        psw=bcrypt.generate_password_hash('mp@gmail.com'+'ciao').decode('utf-8'),
        ))
    conn.commit()"""
    getPortafogliUtente = conn.execute(select(portafoglio).where(portafoglio.c.idUtente == current_user.get_id()).order_by(portafoglio.c.dataInserimento.desc())).fetchall()
    print(getPortafogliUtente)
    print("ho fatto questo")
    return render_template ("/home/home.html",contattiUtente=contattiUtente, getP=getPortafogliUtente, len=len(getPortafogliUtente), contatti=contatti)

@home_bp.route("/delete/<int:id>", methods=['POST'])
@login_required
def removePortafoglio(id):
    print("rimuovo")
    try:
        conn.execute(delete(portafoglio).where(portafoglio.c.idPortafoglio == id))
        conn.commit()

    except Exception as error:
        print(error.__cause__)
    return redirect(url_for('home_bp.home'))

@home_bp.route('/portafoglio/<int:id>')
@login_required
def goToPortafoglio(id):
    print("cviao")
    print(id)
    clienti = conn.execute(select(cliente).where(cliente.c.idPortafoglio == id)).fetchall()
    return render_template("/portafoglio/portafoglio.html", clienti=clienti)

def filterNumber(val):
    if(val is None):
        return None
    
    if(val is String):
        sub = sub.replace(" ", "")
        sub = list(val)
        if(len(sub) == 13 and list(val)[0] == '+'): # esempio '+393453659562' --> 3453659562
            return val[2:]
    
    return str(val)
    
@home_bp.route('/addContatti', methods=['POST'])
@login_required
def addContatti():
    print("sono quya, contatti")
    # Read the File using Flask request
    file = request.files['file']
 
    # Define variable to load the dataframe
    dataframe = openpyxl.load_workbook(file)
    
    # Define variable to read sheet
    dataframe1 = dataframe.active
    
    try:
        for col in range(1, 5):
            list = []
            for row in dataframe1.iter_cols(1, dataframe1.max_column):
                list.append(row[col].value)
            try:
                conn.execute(insert(contatto).values(
                    nome = list[0],
                    idUtente = current_user.get_id(),
                    secondoNome = list[1],
                    cognome = list[2],
                    viaUfficio1 = list[3],
                    viaUfficio2 = list[4],
                    viaUfficio3 = list[5],
                    citta = list[6],
                    provincia = list[7],
                    cap = list[8],
                    #numUfficio = list[9],
                    #numUfficio2 = list[10],
                    telefonoPrincipale = filterNumber(list[11]),
                    faxAbitazione = filterNumber(list[12]),
                    abitazione = list[13],
                    abitazione2 = list[14],
                    cellulare = filterNumber(list[15]),
                    note = list[16],
                    numeroID = list[17],
                    paginaWeb = list[18],
                    email1 = list[19],
                    email2 = list[20]
                ))
            
            except Exception as error:
                print("ERRROREEEEEEEEEEEEEEEEEEEEEEE")
                print(error.__cause__)
        print("okokoko")
        
        conn.commit()
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()
    return redirect(url_for('home_bp.home', variable=0))

@home_bp.route('/addPortafoglio',methods=['POST'])
@login_required
def addPortafoglio():
    print("sono quya")
    # Read the File using Flask request
    file = request.files['file']
 
    # Parse the data as a Pandas DataFrame type
    #data = pandas.read_excel(file)
 
    # Define variable to load the dataframe
    dataframe = openpyxl.load_workbook(file)
    
    # Define variable to read sheet
    dataframe1 = dataframe.active
    
    try:
        res = conn.execute(insert(portafoglio).values(
            idUtente = current_user.get_id(),
            dataInserimento = date.today()
        ))
        print("sono qua 1")
        for col in range(1, dataframe1.max_row):
            list = []
            for row in dataframe1.iter_cols(1, 18):
                list.append(row[col].value)
            print("sono qua 3")
            print(list)
            print(conn.execute(select(presidio.c.idPresidio).where(presidio.c.nome == list[3])).fetchone()[0])
            print(conn.execute(select(tipocliente.c.idTipoCliente).where(tipocliente.c.nome == list[0])).fetchone()[0])
            conn.execute(insert(cliente).values(
                idUtente = current_user.get_id(),
                idPortafoglio = res.lastrowid,
                tipoCliente = conn.execute(select(tipocliente.c.idTipoCliente).where(tipocliente.c.nome == list[0])).fetchone()[0], #da testare
                cf = list[1],
                ragioneSociale = list[2],
                
                presidio = conn.execute(select(presidio.c.idPresidio).where(presidio.c.nome == list[3])).fetchone()[0],
                indirizzoPrincipale = (list[4]),
                comunePrincipale = None,
                capPrincipale = list[6],
                provinciaDescPrincipale = list[7], 
                provinciaSiglaPrincipale = list[8],
                sediTot = (list[9]),
                nLineeTot = (list[10]),
                fisso = (list[11]),
                mobile = (list[12]),
                totale = (list[13]),
                fatturatoCerved = (list[14]),
                clienteOffMobScadenza = (list[15]),
                fatturatoTim = (list[16]),
                dipendenti = (list[17])
            ))
        print("okokoko")
        
        conn.commit()
    except:
        print("rip")
        conn.rollback()
    
    
    return redirect(url_for('portafoglio_bp.home'))

""""
  idUtente = current_user.get_id(),
                idPortafoglio = lastPortafoglio,
                tipoCliente = 1,
                cf = correctValue(list[1],
                ragioneSociale = correctValue(list[2]),
                presidio = 1,
                indirizzoPrincipale = correctValue(list[4]),
                comunePrincipale = 1,
                capPrincipale = correctValue(list[6]),
                provinciaDescPrincipale = correctValue(list[7]),
                provinciaSiglaPrincipale = correctValue(list[8]),
                sediTot = correctValue(list[9]),
                nLineeTot = correctValue(list[10]),
                fisso = correctValue(list[11]),
                mobile = correctValue(list[12]),
                totale = correctValue(list[12]),
                fatturatoCerved = correctValue(list[13]),
                clienteOffMobScadenza = correctValue(list[14]),
                fatturatoTim = correctValue(list[15]),
                dipendenti = correctValue(list[16])"""