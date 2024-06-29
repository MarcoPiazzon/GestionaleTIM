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
def goToPortafoglio(idPort):
    clienti = conn.execute(select(cliente.c.ragioneSociale).where(cliente.c.idPortafoglio == id)).fetchall()
    
    # chiamata da fare successivamente quando verrà cambiata l'interfaccia grafica, permette di ricevere tutte le trattative dato un cliente

    return render_template("/portafoglio/portafoglio.html", clienti=clienti, current_cliente=[], trattative=[], idPort=id)

@portafoglio_bp.route('/getCliente', methods=['POST'])
@login_required
def getCliente():
    idPort = request.form['idPort']
    print("ciuaiaiaia")
    print(current_user.idPort)
    id=request.form['idSearch']
    current_cliente = conn.execute(select(cliente).where(cliente.c.idCliente == id)).fetchone()
    print("test")
    print(current_cliente)
    clienti = conn.execute(select(cliente).where(cliente.c.idPortafoglio == idPort)).fetchall()
    print("test1")
    print(clienti)
    getTrattative = conn.execute(select(trattativa).where(trattativa.c.idCliente == id)).fetchall()
    print(getTrattative)
    t_len = 0
    if(getTrattative is not None):
        t_len = len(getTrattative)
    print("devo fare")
    return render_template("/portafoglio/portafoglio.html", clienti=clienti, current_cliente=current_cliente, current_len=len(current_cliente), trattative=getTrattative, t_len=t_len, idPort=idPort)

@portafoglio_bp.route('/remove/<int:id>', methods=['POST'])
@login_required
def removeTrattativa(id):
    print("test trattativa")
    print(id)

    try:
        print("")
        conn.execute(delete(trattativa).where(trattativa.c.idTrattativa == id))
        conn.commit()
        print("ho fatto")
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()

    return render_template("/portafoglio/portafoglio.html", clienti=[], current_cliente=[], trattative=[])

@portafoglio_bp.route('/add', methods=['POST'])
@login_required
def addCliente():
    try:
        print("addCliente")
        ragioneSociale = request.form['ragioneSociale']
        cf = request.form['cf']
        presidio = request.form['presidio']
        indirizzoPrincipale = request.form['indirizzo']
        capPrincipale = request.form['capPrincipale']
        comunePrincipale = request.form['comunePrincipale']
        sediTot = request.form['sediTot']
        dipendenti = request.form['dipendenti']
        nLineeTot = request.form['nLineeTot']
        fisso = request.form['fisso']
        mobile = request.form['mobile']
        totale = request.form['totale']
        fatturatoCerved = request.form['fatturatoCerved']
        fatturatoTim = request.form['fatturatoTim']
        clienteOffMobScadenza = request.form['clienteOffMobScadenza']

        conn.execute(
            insert(cliente).values(
                idUtente = current_user.get_id(),
                idPortafoglio = current_user.idPort,
                ragioneSociale = ragioneSociale,
                cf = cf,
                #presidio = presidio, gestire la foreign key
                indirizzoPrincipale = indirizzoPrincipale,
                capPrincipale = capPrincipale,
                # comunePrincipale = comunePrincipale, gestire la foreign key
                sediTot = sediTot,
                dipendenti = dipendenti,
                nLineeTot = nLineeTot,
                fisso = fisso,
                mobile = mobile,
                totale = totale,
                fatturatoCerved = fatturatoCerved,
                fatturatoTim = fatturatoTim,
                clienteOffMobScadenza = clienteOffMobScadenza,
            )
        )
        conn.commit()
        print("tutto bvene")
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()
    

    #res.lastrowid, deve caricare questo id
    current_cliente = conn.execute(select(cliente).where(cliente.c.ragioneSociale == ragioneSociale)).fetchone()
    print("test")
    clienti = conn.execute(select(cliente.c.ragioneSociale).where(cliente.c.idPortafoglio == current_user.idPort)).fetchall()
    # da sistemare fase, convertire il valore nel suo relativo valore stringa
    getTrattative = conn.execute(select(trattativa).where(trattativa.c.idCliente == list(current_cliente)[0])).fetchall()
    print(getTrattative)
    return render_template("/portafoglio/portafoglio.html", clienti=clienti, current_cliente=current_cliente, current_len=len(current_cliente), trattative=getTrattative, t_len=len(getTrattative))

@portafoglio_bp.route('/modifyTrattativa/<int:id>', methods=['POST'])
@login_required
def modifyTrattativa(id):
    print("modifiy Trattativa prova")
    print(request.form)
    try:
        #idUtente = request.form['idUtente'] non lo ho
        idCliente = request.form['idClienteModify']
        codiceCtrDigitali = request.form['codiceCtrDigitaliModify']
        codiceSalesHub = request.form['codiceSalesHubModify']
        areaManager = request.form['areaManagerModify']
        zona = request.form['zonaModify'] 
        tipo = request.form['tipoModify']
        nomeOpportunita = request.form['nomeOpportunitaModify']
        dataCreazioneOpportunita = request.form['dataCreazioneOpportunitaModify']
        fix = request.form['fixModify']
        mobile = request.form['mobileModify']
        categoriaOffertaIT = request.form['categoriaOffertaITModify'] 
        it = request.form['itModify']
        lineeFoniaFix = request.form['lineeFoniaFixModify']
        aom = request.form['aomModify']
        mnp = request.form['mnpModify']
        al = request.form['alModify']
        dataChiusura = request.form['dataChiusuraModify']
        fase = request.form['faseModify']
        noteSpecialista = request.form['noteSpecialistaModify']
        probabilita = (request.form['probabilitaModify'])[:-1]
        inPaf = request.form['inPafModify']
        fornitore = request.form['fornitoreModify']
        
        conn.execute(
            update(trattativa).where(trattativa.c.idTrattativa==id).values(
                idUtente = current_user.get_id(),
                idCliente = idCliente,
                codiceCtrDigitali = codiceCtrDigitali,
                codiceSalesHub = codiceSalesHub,
                areaManager = areaManager,
                zona = zona,
                tipo = tipo,
                nomeOpportunita = nomeOpportunita,
                dataCreazioneOpportunita = dataCreazioneOpportunita,
                fix = fix,
                mobile = mobile,
                categoriaOffertaIT = categoriaOffertaIT,
                it = it,
                lineeFoniaFix = lineeFoniaFix,
                aom = aom,
                mnp = mnp,
                al = al,
                dataChiusura = dataChiusura,
                fase = fase,
                noteSpecialista = noteSpecialista,
                probabilita = probabilita,
                inPaf = inPaf,
                fornitore = fornitore
            )
        )
        conn.commit()
        
        print("tutto bvene")
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()

    clienti = conn.execute(select(cliente.c.ragioneSociale).where(cliente.c.idPortafoglio == id)).fetchall()
    
    # chiamata da fare successivamente quando verrà cambiata l'interfaccia grafica, permette di ricevere tutte le trattative dato un cliente

    return render_template("/portafoglio/portafoglio.html", clienti=clienti, current_cliente=[], trattative=[])


@portafoglio_bp.route('/modifyCliente', methods=['POST'])
@login_required
def modifyCliente():
 
    try:
        idCliente = request.form['idCliente']
        ragioneSociale = request.form['ragioneSociale']
        cf = request.form['cf']
        presidio = request.form['presidio']
        indirizzoPrincipale = request.form['indirizzo']
        capPrincipale = request.form['capPrincipale']
        comunePrincipale = request.form['comunePrincipale']
        sediTot = request.form['sediTot']
        dipendenti = request.form['dipendenti']
        nLineeTot = request.form['nLineeTot']
        fisso = request.form['fisso']
        mobile = request.form['mobile']
        totale = request.form['totale']
        fatturatoCerved = request.form['fatturatoCerved']
        fatturatoTim = request.form['fatturatoTim']
        clienteOffMobScadenza = request.form['clienteOffMobScadenza']
        print(idCliente)
        print(sediTot)
        print(type(sediTot))
        

        conn.execute(
            update(cliente).where(cliente.c.idCliente==idCliente).values(
                idCliente = idCliente,
                ragioneSociale = ragioneSociale,
                cf = cf,
                #presidio = presidio, gestire la foreign key
                indirizzoPrincipale = indirizzoPrincipale,
                capPrincipale = capPrincipale,
                # comunePrincipale = comunePrincipale, gestire la foreign key
                sediTot = sediTot,
                dipendenti = dipendenti,
                nLineeTot = nLineeTot,
                fisso = fisso,
                mobile = mobile,
                totale = totale,
                fatturatoCerved = fatturatoCerved,
                fatturatoTim = fatturatoTim,
                clienteOffMobScadenza = clienteOffMobScadenza,
            )
        )
        conn.commit()
        print("tutto bvene")
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()

    current_cliente = conn.execute(select(cliente).where(cliente.c.ragioneSociale == ragioneSociale)).fetchone()
    print("test")
    clienti = conn.execute(select(cliente.c.ragioneSociale).where(cliente.c.idPortafoglio == id)).fetchall()
    # da sistemare fase, convertire il valore nel suo relativo valore stringa
    getTrattative = conn.execute(select(trattativa).where(trattativa.c.idCliente == list(current_cliente)[0])).fetchall()
    print(getTrattative)
    return render_template("/portafoglio/portafoglio.html", clienti=clienti, len=len(clienti), current_cliente=current_cliente, current_len=len(current_cliente), trattative=getTrattative, t_len=len(getTrattative))


def getFase(andtra, value):
    for v in andtra:
        if(value == v[1]):
            return v[0]

def getCategoria(getCateOff, value):
    for v in getCateOff:
        if(value == v[1]):
            return v[0]

@portafoglio_bp.route('/addTrattativaForm', methods=['POST'])
@login_required
def addTrattativaForm():
    try:
        print("addTrattattiva")
        print(current_user.get_id())
        print(type(current_user.get_id()))
        print(request.form['idClienteAdd'])
        print(request.form)
        idUtente = 2
        idCliente = request.form['idClienteAdd']
        codiceCtrDigitali = request.form['codiceCtrDigitaliAdd']
        codiceSalesHub = request.form['codiceSalesHubAdd']
        areaManager = request.form['areaManagerAdd']
        zona = request.form['zonaAdd']
        tipo = request.form['tipoAdd']
        nomeOpportunita = request.form['nomeOpportunitaAdd']
        dataChiusuraOpportunita = request.form['dataCreazioneOpportunitaAdd']
        print("test data")
        print(dataChiusuraOpportunita)
        fix = request.form['fixAdd']
        mobile = request.form['mobileAdd']
        categoriaOffertaIT = request.form['categoriaOffertaITAdd']
        it = request.form['itAdd']
        lineeFoniaFix = request.form['lineeFoniaFixAdd']
        aom = request.form['aomAdd']
        mnp = request.form['mnpAdd']
        al = request.form['alAdd']
        dataChiusura = request.form['dataChiusuraAdd']
        fase = request.form['faseAdd']
        noteSpecialista = request.form['noteSpecialistaAdd']
        probabilita = request.form['probabilitaAdd']
        inPaf = request.form['inPafAdd']
        fornitore = request.form['fornitoreAdd']
        
        
        conn.execute(insert(trattativa).values(
            idUtente = 2,
            idCliente = 6,
            codiceCtrDigitali = codiceCtrDigitali,
            codiceSalesHub = codiceSalesHub,
            areaManager = areaManager,
            zona = zona,
            tipo = tipo,
            nomeOpportunita = nomeOpportunita,
            dataCreazioneOpportunita = dataChiusuraOpportunita,
            fix = fix,
            mobile = mobile,
            categoriaOffertaIT = categoriaOffertaIT,
            it = it,
            lineeFoniaFix = lineeFoniaFix,
            aom = aom,
            mnp = mnp,
            al = al,
            dataChiusura = dataChiusura,
            fase = fase,
            noteSpecialista = noteSpecialista,
            probabilita = probabilita,
            inPaf = inPaf,
            fornitore = fornitore
        ))
        conn.commit()
        
        print("tutto bene add")
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()
    
    clienti = conn.execute(select(cliente.c.ragioneSociale).where(cliente.c.idPortafoglio == id)).fetchall()
    
    # chiamata da fare successivamente quando verrà cambiata l'interfaccia grafica, permette di ricevere tutte le trattative dato un cliente

    return render_template("/portafoglio/portafoglio.html", clienti=clienti, current_cliente=[], trattative=[], idPort=id)

@portafoglio_bp.route('/addTrattativa',methods=['POST'])
@login_required
def addPortafoglio():
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
                    dataCreazioneOpportunita = list[8], # da testare
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
                    probabilita = (list[20])*100,
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
    return render_template("/portafoglio/portafoglio.html", clienti=[], trattative =[]) 

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