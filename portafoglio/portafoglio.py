from portafoglio import portafoglio_bp
from flask import Blueprint,render_template, url_for, redirect, request, Response
from flask_login import *
from home import *
from model import *
import openpyxl
from datetime import date
import io
import xlwt
import psycopg2
import psycopg2.extras

#idPort: idPortafoglio
#id: idCliente
@portafoglio_bp.route('/<int:idPort>/<int:id>')
def home(idPort, id):
    print("dentro home portafoglio")
    print(idPort)
    print(id)
    print(type(idPort))
    print(type(id))
    print(id is None)
    current_user.idPort = idPort
    clienti = None
    current_cliente = None
    trattative = None 
    t_len = 0
    categorie = conn.execute(select(categoria)).fetchall()
    andamento = conn.execute(select(andamentotrattativa)).fetchall()
    if(idPort != 0):
        #fare la query in modo che prenda solo ragioneSociale e idCliente (ora lo fa)
        clienti = conn.execute(select(cliente.c.ragioneSociale, cliente.c.idCliente).where(cliente.c.idPortafoglio == idPort)).fetchall()
    if(id != 0):
        current_cliente = conn.execute(select(cliente).where(cliente.c.idCliente == id)).fetchone()
        trattative = conn.execute(select(trattativa).where(trattativa.c.idCliente == id)).fetchall()
        print(current_cliente)
        print(trattative)
        
        
        if not (trattative is None):
            #select appuntamento.titolo, trattativa.nomeOpportunita from ((appuntamento join trattativaappuntamento on appuntamento.idAppuntamento = trattativaappuntamento.idAppuntamento)
            #join trattativa on trattativa.idTrattativa = trattativaappuntamento.idTrattativa)
            t_len = len(trattative)
            print(type(trattative))
            for i in range(0, t_len):

                appuntamenti = conn.execute(select(appuntamento.c.titolo).select_from(join(appuntamento,join(trattativaappuntamento,trattativa, trattativaappuntamento.c.idTrattativa == trattativa.c.idTrattativa), appuntamento.c.idAppuntamento == trattativaappuntamento.c.idAppuntamento)).where(trattativa.c.idTrattativa == trattative[i][0])).fetchall()
                print(appuntamenti)
                trattative[i] = list(trattative[i])
                if not (appuntamenti is None):
                    
                    
                    trattative[i].append(appuntamenti)
                    print(trattative[i][25])
            #print(len(trattative[0]))
            #print(trattative)
    return render_template ("/portafoglio/portafoglio.html", clienti=clienti, current_cliente=current_cliente, trattative=trattative, t_len=t_len, idPort=idPort, categorie=categorie, andamento=andamento)


@portafoglio_bp.route('/portafoglio/<int:id>')
@login_required
def goToPortafoglio(id):
    # chiamata da fare successivamente quando verrà cambiata l'interfaccia grafica, permette di ricevere tutte le trattative dato un cliente
    return home(id, 0)

@portafoglio_bp.route('/getCliente', methods=['POST'])
@login_required
def getCliente():
    #print(request.form)
    idPort = request.form['idPort']
    id=request.form['idSearch']
    
    return home(idPort, id)

@portafoglio_bp.route('/remove/<int:id>', methods=['POST'])
@login_required
def removeTrattativa(id):
    print("test trattativa")
    print(id)
    getIdCliente = conn.execute(select(trattativa.c.idCliente).where(trattativa.c.idTrattativa == id)).fetchone()[0]
    try:
        print("")
        conn.execute(delete(trattativa).where(trattativa.c.idTrattativa == id))

        #appuntamenti = conn.execute(select(trattativaappuntamento).where(trattativa.c.idTrattativa == id)).fetchall()

        #if not (appuntamenti is None):
         #   for a in appuntamenti:
          #      conn.execute(delete(appuntamenti).where(appuntamenti.c.idAppuntamento == a.idAppuntamento))

        conn.commit()
        print("ho fatto")
    except Exception as error:
        print("rip")
        print(error.__cause__)
        conn.rollback()
    
    return home(current_user.idPort, getIdCliente)

@portafoglio_bp.route('/add', methods=['POST'])
@login_required
def addCliente():
    try:
        print("addCliente")
        idPort = request.form['idPort']
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
                idPortafoglio = idPort,
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
    idCliente = conn.execute(select(cliente.c.idCliente).where(cliente.c.ragioneSociale == ragioneSociale)).fetchone()[0]
    
    return home(idPort, idCliente)

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


    return home(current_user.idPort, idCliente)


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

    return home(current_user.idPort, idCliente)

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
            idCliente = idCliente,
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
    
    return home(current_user.idPort, idCliente)

@portafoglio_bp.route('/addTrattativa',methods=['POST'])
@login_required
def addPortafoglio():
    # Read the File using Flask request
    file = request.files['file']
    idCliente = request.form['addTrattativaIdCliente']
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
        for col in range(1, 4):
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
    return home(current_user.get_id(), 0)

@portafoglio_bp.route('/getExcel/<int:id>')
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
        
@portafoglio_bp.route('/getExcelTrattative/<int:id>')
def getExcelTrattative(id):
    print(id)
    res = conn.execute(select(trattativa)).fetchall()

    output = io.BytesIO()

    workbook = xlwt.Workbook()

    sh = workbook.add_sheet('Report Portafoglio')
    style0 = xlwt.easyxf('pattern: pattern solid, fore_colour red')
    sh.write(0,0,'CODICE CTR DIGITALE',style0)
    sh.write(0,1,'CODICE SALES HUB')
    sh.write(0,2,'AREA MANAGER')
    sh.write(0,3,'SA')
    sh.write(0,4,'RAGIONE SOCIALE')
    sh.write(0,5,'ZONA')
    sh.write(0,6,'TIPO')
    sh.write(0,7,'NOME OPPORTUNITA')
    sh.write(0,8,'DATA CREAZIONE OPPORTUNITA')
    sh.write(0,9,'FIX (€)')
    sh.write(0,10,'MOBILE(€)')
    sh.write(0,11,'CATEGORIA OFFERTA IT')
    sh.write(0,12,'IT')
    sh.write(0,13,'LINEE FONIA FIX')
    sh.write(0,14,'AOM')
    sh.write(0,15,'MNP')
    sh.write(0,16,'AL')
    sh.write(0,17,'DATA CHIUSURA')
    sh.write(0,18,'FASE')
    sh.write(0,19,'NOTE SPECIALISTA')
    sh.write(0,20,'PROBABILITA')
    sh.write(0,21,'IN PAF')
    sh.write(0,22,'FORNITORE')

    idx = 0
    for row in res:
        print(row)
        sh.write(idx+1, 0, row['codiceCtrDigitali'])
        sh.write(idx+1, 1, row['codiceSalesHub'])
        sh.write(idx+1, 2, row['areaManager'])
        sh.write(idx+1, 3, 'SALVATORE IACCARINO')
        sh.write(idx+1, 4, 'NOME CLIENTE')
        sh.write(idx+1, 5, row['zona'])
        sh.write(idx+1, 6, row['tipo'])
        sh.write(idx+1, 7, row['nomeOpportunita'])
        sh.write(idx+1, 8, row['dataCreazioneOpportunita'])
        sh.write(idx+1, 9, row['fix'])
        sh.write(idx+1, 10, row['mobile'])
        sh.write(idx+1, 11, row['categoriaOffertaIT'])
        sh.write(idx+1, 12, row['it'])
        sh.write(idx+1, 13, row['lineeFoniaFix'])
        sh.write(idx+1, 14, row['aom'])
        sh.write(idx+1, 15, row['mnp'])
        sh.write(idx+1, 16, row['al'])
        sh.write(idx+1, 17, row['dataChiusura'])
        sh.write(idx+1, 18, row['fase'])
        sh.write(idx+1, 19, row['noteSpecialista'])
        sh.write(idx+1, 20, row['probabilita'])
        sh.write(idx+1, 21, row['inPaf'])
        sh.write(idx+1, 22, row['fornitore'])
        idx += 1


    workbook.save(output)
    output.seek(0)
    
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=pipeline.xls"})
   
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