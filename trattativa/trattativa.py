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
    clienti = conn.execute(select(cliente.c.ragioneSociale, cliente.c.idCliente).where(cliente.c.idPortafoglio == id)).fetchall()
    trattative = conn.execute(select(trattativa, andamentotrattativa.c.nome, categoria.c.nome, cliente.c.ragioneSociale)
                    .join(cliente)
                    .outerjoin(andamentotrattativa)
                    .outerjoin(categoria)
                    .where(trattativa.c.idUtente == current_user.get_id())
                    .where(cliente.c.idPortafoglio == id)
                    .order_by(trattativa.c.nomeOpportunita)).fetchall()
    
    print(len(trattative))
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
            print(trattative[i])
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

            appuntamenti = conn.execute(select(appuntamento.c.titolo, appuntamento.c.dataApp).select_from(join(appuntamento,join(trattativaappuntamento,trattativa, trattativaappuntamento.c.idTrattativa == trattativa.c.idTrattativa), appuntamento.c.idAppuntamento == trattativaappuntamento.c.idAppuntamento)).where(trattativa.c.idTrattativa == trattative[i][0]).where(appuntamento.c.dataApp >= todays_datetime).order_by(appuntamento.c.dataApp)).fetchall()
            
            #print(appuntamenti)
            #print(type(appuntamenti))
            trattative[i] = list(trattative[i])
            if (len(appuntamenti) > 0):
                print("Ho appuntamento")    
                
                trattative[i].append(appuntamenti)
                print(trattative[i][25])

            print(len(trattative[i]))
    categorie = conn.execute(select(categoria)).fetchall()
    andamento = conn.execute(select(andamentotrattativa)).fetchall()
    print("dopo")
    print(len(trattative))
    print(tratVinte)
    print(tratVinteMoney)
    print(tratPerse)
    return render_template ("/trattativa/trattativa.html",trattative = trattative, t_len = t_len, categorie = categorie, andamento = andamento, tratVinte = tratVinte, tratPerse = tratPerse, tratVinteMoney = tratVinteMoney, clienti = clienti)

@trattativa_bp.route('/modifyTrattativa/<int:id>', methods=['POST'])
@login_required
def modifyTrattativa(id):
    print("modifiy Trattativa prova")
    print(request.form)
    try:
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


    return redirect(url_for('.home', id = current_user.idPort))


@trattativa_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def removeTrattativa(id):
    print("REMOVE TRATTATIVA")
    print(current_user.idPort)
    try:
        conn.execute(delete(trattativa).where(trattativa.c.idTrattativa == id))
        conn.execute(delete(trattativaappuntamento).where(trattativaappuntamento.c.idTrattativa == id))
        conn.commit()
    except Exception as error:
        conn.rollback()
        print("rip")
        print(error)
        print(error.__cause__)   
    
    return redirect(url_for('.home',id = current_user.idPort))