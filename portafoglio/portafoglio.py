from portafoglio import portafoglio_bp
from flask import Blueprint,render_template, url_for, redirect, request
from flask_login import *
from home import *
from model import *
import openpyxl
from datetime import date
@portafoglio_bp.route('/')
def home():
    return render_template ("/portafoglio/portafoglio.html")


@portafoglio_bp.route('/portafoglio/<int:id>')
@login_required
def goToPortafoglio(id):
    
    clienti = conn.execute(select(cliente).where(cliente.c.idPortafoglio == id)).fetchall()
    
    #getTrattative = conn.execute(select(trattativa).where(trattativa.c.idCliente == cliente.c.id)).fetchall()  
    # chiamata da fare successivamente quando verrà cambiata l'interfaccia grafica, permette di ricevere tutte le trattative dato un cliente
    print(clienti)
    return render_template("/portafoglio/portafoglio.html", clienti=clienti, len=len(clienti))


def getFase(andtra, value):
    for v in andtra:
        if(value == v[1]):
            return v[0]

def getCategoria(getCateOff, value):
    for v in getCateOff:
        if(value == v[1]):
            return v[0]

@portafoglio_bp.route('/addTrattativa',methods=['POST'])
@login_required
def addPortafoglio():
    print("sono quya")
    # Read the File using Flask request
    file = request.files['file']
 
    # Parse the data as a Pandas DataFrame type
    #data = pandas.read_excel(file)
 
    # Define variable to load the dataframe
    dataframe = openpyxl.load_workbook(file, data_only=True)
    
    # Define variable to read sheet
    dataframe1 = dataframe.active
    
    try:
        print("sono qua 1")
        print(dataframe1.max_row)
        print(String(None))
        andtra = conn.execute(select(andamentotrattativa)).fetchall()
        getCateOff = conn.execute(select(categoria)).fetchall()
        print(getFase(andtra, "IN TRATTATIVA"))
        print("dopo")
        for col in range(1, dataframe1.max_row):
            list = []
            checkRow = True
            for row in dataframe1.iter_cols(1, dataframe1.max_column):
                if(row[col].value is not None):
                    checkRow = False
                    print((row[col].value), end= ", ")
                list.append(row[col].value)
            print()
            if(checkRow == False):
                conn.execute(insert(trattativa).values(
                    idUtente = current_user.get_id(),
                    idCliente = conn.execute(select(cliente.c.idCliente).where(list[4] == cliente.c.ragioneSociale)).fetchone()[0], #fare query che trova il nome e assegna l'id nella tabella cliente
                    codiceCtrDigitali = list[0],
                    codiceSalesHub = list[1],
                    areaManager = list[2],
                    zona = list[5],
                    tipo = (list[6]),
                    nomeOpportunita = list[7],
                    dataCreazioneOpportunita = None,
                    fix = list[9],
                    mobile = list[10],
                    categoriaOffertaIT = getCategoria(getCateOff, list[11]),
                    it = (list[12]),
                    lineeFoniaFix = (list[13]),
                    aom = (list[14]),
                    mnp = (list[15]),
                    al = (list[16]),
                    dataChiusura = (list[17]),
                    fase = getFase(andtra, list[18])  ,
                    noteSpecialista = (list[19]),
                    probabilita = list[20],
                    inPaf = None,
                    record = list[22],
                    fornitore = list[23],
                ))
        print("okokoko")
        
        conn.commit()
    except:
        print("rip trattative")
        conn.rollback()
    # Iterate the loop to read the cell values

    # Return HTML snippet that will render the table
    
    
    return render_template("/portafoglio/portafoglio.html", clienti=[]) 

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