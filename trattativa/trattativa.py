from flask import Blueprint,render_template, url_for, redirect, request, Response
from trattativa import *
from flask_login import *
from model import *
from login.login import bcrypt
import openpyxl
from datetime import datetime


@trattativa_bp.route('/<int:id>', methods=['GET', 'POST'])
def home(id):
    #trattative = conn.execute(
    #   select(trattativa, andamentotrattativa.c.nome, categoria.c.nome).
    #        select_from(
    #            outerjoin(categoria ,
    #                outerjoin(cliente, 
    #                    outerjoin(trattativa, andamentotrattativa, trattativa.c.fase == andamentotrattativa.c.idAndamento),
    #                cliente.c.idCliente == trattativa.c.idCliente), 
    #            categoria.c.idCategoria == trattativa.c.categoriaOffertaIT)
    #        ).where(trattativa.c.idUtente == current_user.get_id()).where(cliente.c.idPortafoglio == id)
    #).fetchall()
    tratVinte= 0
    tratPerse = 0
    tratVinteMoney = 0
    clienti = conn.execute(select(cliente.c.ragionesociale, cliente.c.idcliente).where(cliente.c.idportafoglio == id)).fetchall()
    trattative = conn.execute(select(trattativa, andamentotrattativa.c.nome, categoria.c.nome, cliente.c.ragionesociale)
                    .join(cliente)
                    .outerjoin(andamentotrattativa)
                    .outerjoin(categoria)
                    .order_by(trattativa.c.nomeopportunita)).fetchall()
    
    #print(len(trattative))
    t_len = 0
    if not (trattative is None):
        #select appuntamento.titolo, trattativa.nomeOpportunita from ((appuntamento join trattativaappuntamento on appuntamento.idAppuntamento = trattativaappuntamento.idAppuntamento)
        #join trattativa on trattativa.idTrattativa = trattativaappuntamento.idTrattativa)
        t_len = len(trattative)
        
        #print(type(trattative))
        todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day, datetime.today().hour, datetime.today().minute, datetime.today().second)
        yesterday = datetime(2024,7,10)
        #print(todays_datetime > yesterday)
        #print(todays_datetime)            
        for i in range(0, t_len):
            #test per vedere le trattative vinte
            #print(trattative[i])
            if(trattative[i][25].upper() == "VINTA"):
                tratVinte += 1 
                if not (trattative[i][10] is None):
                    tratVinteMoney += trattative[i][10]
                if not (trattative[i][11] is None):
                    tratVinteMoney += trattative[i][11]
                if not (trattative[i][13] is None):
                    tratVinteMoney += trattative[i][13]

            if(trattative[i][25].upper() == "PERSA"):
                tratPerse += 1

            appuntamenti = conn.execute(select(appuntamento.c.titolo, appuntamento.c.dataapp).select_from(join(appuntamento,join(trattativaappuntamento,trattativa, trattativaappuntamento.c.idtrattativa == trattativa.c.idtrattativa), appuntamento.c.idappuntamento == trattativaappuntamento.c.idappuntamento)).where(trattativa.c.idtrattativa == trattative[i][0]).where(appuntamento.c.dataapp >= todays_datetime).order_by(appuntamento.c.dataapp)).fetchall()
            
            #print(appuntamenti)
            #print(type(appuntamenti))
            trattative[i] = list(trattative[i])
            if (len(appuntamenti) > 0):
                print("Ho appuntamento")    
                
                trattative[i].append(appuntamenti)
                print(trattative[i][25])

            #print(len(trattative[i]))
    categorie = conn.execute(select(categoria)).fetchall()
    andamento = conn.execute(select(andamentotrattativa)).fetchall()
    print("dopo")
    print(len(trattative))
    print(tratVinte)
    print(tratVinteMoney)
    print(tratPerse)
    return render_template ("/trattativa/trattativa.html",trattative = trattative, t_len = t_len, categorie = categorie, andamento = andamento, tratVinte = tratVinte, tratPerse = tratPerse, tratVinteMoney = tratVinteMoney, clienti = clienti)

def checkDate(val):
    if(isinstance(val, str)):
        if val == '':
            return None
        else: 
            return val 

def checkNull(val):
    print(type(val))
    if(isinstance(val, str)):
        if val == '':
            return 0
        else: 
            return val
    return val

@trattativa_bp.route('/modifyTrattativa/<int:id>', methods=['POST'])
@login_required
def modifyTrattativa(id):
    print("modifiy Trattativa prova")
    try:
        idcliente = request.form['idClienteModify']
        codicectrdigitali = request.form['codiceCtrDigitaliModify']
        codicesaleshub = request.form['codiceSalesHubModify']
        zona = request.form['zonaModify'] 
        tipo = request.form['tipoModify']
        nomeopportunita = request.form['nomeOpportunitaModify']
        datacreazioneopportunita = checkDate(request.form['dataCreazioneOpportunitaModify']),
        fix = checkNull(request.form['fixModify'])
        mobile = checkNull(request.form['mobileModify'])
        categoriaoffertait = request.form['categoriaOffertaITModify'] 
        it = checkNull(request.form['itModify'])
        lineefoniafix = checkNull(request.form['lineeFoniaFixModify'])
        aom = checkNull(request.form['aomModify'])
        mnp = checkNull(request.form['mnpModify'])
        al = checkNull(request.form['alModify'])
        datachiusura = checkDate(request.form['dataChiusuraModify'])
        
        fase = request.form['faseModify']
        notespecialista = request.form['noteSpecialistaModify']
        probabilita = checkNull(request.form['probabilitaModify'])
        if not (probabilita is None):
            if(isinstance(probabilita,str) and '%' in probabilita):
                probabilita = probabilita[:-1]
        inPaf = request.form['inPafModify']
        fornitore = request.form['fornitoreModify']
        
        conn.execute(
            update(trattativa).where(trattativa.c.idtrattativa==id).values(
                idutente = current_user.get_id(),
                idcliente = idcliente,
                codicectrdigitali = codicectrdigitali,
                codicesaleshub = codicesaleshub,
                zona = zona,
                tipo = tipo,
                nomeopportunita = nomeopportunita,
                datacreazioneopportunita = datacreazioneopportunita,
                fix = fix,
                mobile = mobile,
                categoriaoffertait = categoriaoffertait,
                it = it,
                lineefoniafix = lineefoniafix,
                aom = aom,
                mnp = mnp,
                al = al,
                datachiusura = datachiusura,
                fase = fase,
                notespecialista = notespecialista,
                probabilita = probabilita,
                inpaf = 1,
                fornitore = fornitore
            )
        )
        
        print("tutto bvene")
    except Exception as error:
        print("rip")
        print(error)
        print(error.__cause__)
        conn.rollback()


    return redirect(url_for('.home', id = current_user.idPort))


@trattativa_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def removeTrattativa(id):
    print("REMOVE TRATTATIVA")
    print(current_user.idPort)
    try:
        conn.execute(delete(trattativa).where(trattativa.c.idtrattativa == id))
        conn.execute(delete(trattativaappuntamento).where(trattativaappuntamento.c.idtrattativa == id))
    except Exception as error:
        conn.rollback()
        print("rip")
        print(error)
        print(error.__cause__)   
    
    return redirect(url_for('.home',id = current_user.idPort))