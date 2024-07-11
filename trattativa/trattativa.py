from flask import Blueprint,render_template, url_for, redirect, request, Response
from trattativa import *
from flask_login import *
from model import *
from login.login import bcrypt
import openpyxl
from datetime import date

@trattativa_bp.route('/<int:id>', methods=['GET', 'POST'])
def home(id):
    trattative = conn.execute(
        select(trattativa, andamentotrattativa.c.nome, categoria.c.nome).
            select_from(
                join(categoria ,
                    join(cliente, 
                        join(trattativa, andamentotrattativa, trattativa.c.fase == andamentotrattativa.c.idAndamento),
                    cliente.c.idCliente == trattativa.c.idCliente), 
                categoria.c.idCategoria == trattativa.c.categoriaOffertaIT)
            ).where(cliente.c.idUtente == current_user.get_id() and cliente.c.idPortafoglio == id)
    ).fetchall()
    t_len = 0
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

    print(trattative)
    categorie = conn.execute(select(categoria)).fetchall()
    andamento = conn.execute(select(andamentotrattativa)).fetchall()
    return render_template ("/trattativa/trattativa.html",trattative = trattative, t_len = t_len, categorie = categorie, andamento = andamento)
