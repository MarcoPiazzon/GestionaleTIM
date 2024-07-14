from flask import Blueprint,render_template, url_for, redirect, request, Response
from home import *
from flask_login import *
from model import *
from login.login import bcrypt
import openpyxl
from datetime import date
import io
import xlwt
import psycopg2
import psycopg2.extras
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

titolo = "Home"
@home_bp.route('/', methods=['GET', 'POST'])
def home():
    contatti = conn.execute(select(contatto).where(contatto.c.idUtente == current_user.get_id())).fetchall()
    
    """conn.execute(insert(utente).values(
        nome = 'Marco',
        cognome= 'Piazzon',
        email= 'mp@gmail.com',
        psw=bcrypt.generate_password_hash('mp@gmail.com'+'ciao').decode('utf-8'),
        ))
    conn.commit()"""
    getPortafogliUtente = conn.execute(select(portafoglio).where(portafoglio.c.idUtente == current_user.get_id()).order_by(portafoglio.c.dataInserimento.desc())).fetchall()
    getPortafogliUtente = list(getPortafogliUtente)
    print(getPortafogliUtente)
    print(type(getPortafogliUtente))
    print("ho fatto questo")
    return render_template ("/home/home.html", getP=getPortafogliUtente, len=len(getPortafogliUtente), titolo=titolo)

@home_bp.route("/delete/<int:id>", methods=['POST','GET'])
@login_required
def removePortafoglio(id):
    print("rimuovo")
    print("sto cancellando")
    print(id)

    return redirect(url_for('home_bp.home'))

@home_bp.route('/portafoglio/<int:id>')
@login_required
def goToPortafoglio(id, message):
    print("cviao")
    print(id)
    clienti = conn.execute(select(cliente).where(cliente.c.idPortafoglio == id)).fetchall()
    return render_template("/portafoglio/portafoglio.html", clienti=clienti, message = message, titolo ="Portafoglio")

def filterNumber(val):
    if(val is None):
        return None
    
    if(val is String):
        sub = sub.replace(" ", "")
        sub = list(val)
        if(len(sub) == 13 and list(val)[0] == '+'): # esempio '+393453659562' --> 3453659562
            return val[2:]
    
    return str(val)


def getFase(andtra, value):
    for v in andtra:
        if(value == v[1]):
            return v[0]
    return None

def getCategoria(getCateOff, value):
    for v in getCateOff:
        if(value == v[1]):
            return v[0]
    return None

@home_bp.route('/addPortafoglio',methods=['POST'])
@login_required
def addPortafoglio():
    warnings.simplefilter(action='ignore', category=UserWarning)
    print("sono quya")
    # Read the File using Flask request
    file = request.files['fileDoc']
 
    # Parse the data as a Pandas DataFrame type
    #data = pandas.read_excel(file)
 
    # Define variable to load the dataframe
    dataframe = openpyxl.load_workbook(file)
    
    # Define variable to read sheet
    dataframe1 = dataframe.active

    file2 = request.files['filePipeline']
    # Parse the data as a Pandas DataFrame type
    #data = pandas.read_excel(file)
 
    # Define variable to load the dataframe
    dataframe2 = openpyxl.load_workbook(file2, data_only=True)
    
    # Define variable to read sheet
    dataframe3 = dataframe2.active


    id = 0
    try:
        res = conn.execute(insert(portafoglio).values(
            idUtente = current_user.get_id(),
            dataInserimento = date.today()
        ))
        id = res.inserted_primary_key[0]
        print("test della vita")
        print(id)
        print("sono qua 1")
        for col in range(1, dataframe1.max_row):
            listapp = []
            for row in dataframe1.iter_cols(1, dataframe1.max_column):
                listapp.append(row[col].value)
           # print("sono qua 3")
           # print(listapp)
           # print(conn.execute(select(presidio.c.idPresidio).where(presidio.c.nome == listapp[3])).fetchone()[0])
           # print(conn.execute(select(tipocliente.c.idTipoCliente).where(tipocliente.c.nome == listapp[0])).fetchone()[0])
            conn.execute(insert(cliente).values(
                idUtente = current_user.get_id(),
                idPortafoglio = res.lastrowid,
                tipoCliente = conn.execute(select(tipocliente.c.idTipoCliente).where(tipocliente.c.nome == listapp[0])).fetchone()[0], #da testare
                cf = listapp[1],
                ragioneSociale = listapp[2],
                
                presidio = conn.execute(select(presidio.c.idPresidio).where(presidio.c.nome == listapp[3])).fetchone()[0],
                indirizzoPrincipale = (listapp[4]),
                comunePrincipale = None,
                capPrincipale = listapp[6],
                provinciaDescPrincipale = listapp[7], 
                provinciaSiglaPrincipale = listapp[8],
                sediTot = (listapp[9]),
                nLineeTot = (listapp[10]),
                fisso = (listapp[11]),
                mobile = (listapp[12]),
                totale = (listapp[13]),
                fatturatoCerved = (listapp[14]),
                clienteOffMobScadenza = (listapp[15]),
                fatturatoTim = (listapp[16]),
                dipendenti = (listapp[17])
            ))
        print("okokoko")
        print("sono qua 1")
        print(dataframe3.max_row)
        print(String(None))
        andtra = conn.execute(select(andamentotrattativa)).fetchall()
        getCateOff = conn.execute(select(categoria)).fetchall()
        print(getFase(andtra, "IN TRATTATIVA"))
        print("dopo")
        for col in range(1, dataframe3.max_row):
            listapp = []
            checkRow = True
            for row in dataframe3.iter_cols(1, dataframe3.max_column):
                if(row[col].value is not None):
                    checkRow = False
                   # print((row[col].value), end= ", ")
                listapp.append(row[col].value)
            print()
            if(checkRow == False):
              #  print("sto testando id")
              #  print(id)
                idlist = conn.execute(select(cliente.c.idCliente).where(listapp[4] == cliente.c.ragioneSociale and cliente.c.idPortafoglio == id)).fetchall()
                idlist = list(idlist)
                numero = idlist[-1]
                prob = None
                if(listapp[20]):
                    prob = listapp[20]*100
                conn.execute(insert(trattativa).values(
                    idUtente = current_user.get_id(),
                    idCliente = numero[0], #fare query che trova il nome e assegna l'id nella tabella cliente
                    codiceCtrDigitali = listapp[0],
                    codiceSalesHub = listapp[1],
                    areaManager = listapp[2],
                    zona = listapp[5],
                    tipo = (listapp[6]),
                    nomeOpportunita = listapp[7],
                    dataCreazioneOpportunita = listapp[8], # da testare
                    fix = listapp[9],
                    mobile = listapp[10],
                    categoriaOffertaIT = getCategoria(getCateOff, listapp[11]),
                    it = (listapp[12]),
                    lineeFoniaFix = (listapp[13]),
                    aom = (listapp[14]),
                    mnp = (listapp[15]),
                    al = (listapp[16]),
                    dataChiusura = (listapp[17]),
                    fase = getFase(andtra, listapp[18])  ,
                    noteSpecialista = (listapp[19]),
                    probabilita = prob,
                    inPaf = None,
                    record = listapp[22],
                    fornitore = listapp[23],
                ))
        print("okokoko")
        global message
        message = "Portafoglio creato"
        conn.commit()
    except Exception as error:
        print("rip")
        print(error)
        print(error.__cause__)
        conn.rollback()
    
    clienti = conn.execute(select(cliente).where(cliente.c.idPortafoglio == id)).fetchall()
    return render_template("/portafoglio/portafoglio.html", clienti=clienti, message = message, titolo ="Portafoglio")


@home_bp.route('/getExcel/<int:id>')
def getExcel(id):
    print("sto creando il file")
    print(id)
    res = conn.execute(select(cliente).where(cliente.c.idPortafoglio == id)).fetchall()

    output = io.BytesIO()

    workbook = xlwt.Workbook()

    sh = workbook.add_sheet('Report Portafoglio')

    sh.write(0,0,'TIPO CLIENTE')
    sh.write(0,1,'CF')
    sh.write(0,2,'RAG_SOC_CLI')
    sh.write(0,3,'PRESIDIO')
    sh.write(0,4,'INDIRIZZO PRINCIPALE')
    sh.write(0,5,'COMUNE_PRINCIPALE')
    sh.write(0,6,'CAP_PRINCIPALE')
    sh.write(0,7,'PROVINCIA_DESCR_PRINCIPALE')
    sh.write(0,8,'PROVINCIA_SIGLA_PRINCIPALE')
    sh.write(0,9,'SEDI_TOT')
    sh.write(0,10,'N_LINEE_TOT')
    sh.write(0,11,'_FISSO')
    sh.write(0,12,'_MOBILE')
    sh.write(0,13,'_TOTALE')
    sh.write(0,14,'FATTURATO_CERVED')
    sh.write(0,15,'CLIENTE_OFF_MOB_SCADENZA')
    sh.write(0,16,'FATTURATO_IT_TIM')
    sh.write(0,17,'DIPENDENTI')

    idx = 0
    for row in res:
        print(row)
        sh.write(idx+1, 0, row['tipoCliente'])
        sh.write(idx+1, 1, row['cf'])
        sh.write(idx+1, 2, row['ragioneSociale'])
        sh.write(idx+1, 3, row['presidio'])
        sh.write(idx+1, 4, row['indirizzoPrincipale'])
        sh.write(idx+1, 5, row['comunePrincipale'])
        sh.write(idx+1, 6, row['capPrincipale'])
        sh.write(idx+1, 7, row['provinciaDescPrincipale'])
        sh.write(idx+1, 8, row['provinciaSiglaPrincipale'])
        sh.write(idx+1, 9, row['sediTot'])
        sh.write(idx+1, 10, row['nLineeTot'])
        sh.write(idx+1, 11, row['fisso'])
        sh.write(idx+1, 12, row['mobile'])
        sh.write(idx+1, 13, row['totale'])
        sh.write(idx+1, 14, row['fatturatoCerved'])
        sh.write(idx+1, 15, row['clienteOffMobScadenza'])
        sh.write(idx+1, 16, row['fatturatoTim'])
        sh.write(idx+1, 17, row['dipendenti'])
        idx += 1
    
    workbook.save(output)
    output.seek(0)
    
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=report_portafoglio.xls"})
        
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