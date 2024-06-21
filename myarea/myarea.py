from flask import render_template,make_response, url_for, redirect,flash,request,abort
from myarea import *
from flask_login import *
from model import *
import traceback
from datetime import date

@myarea_bp.route('/', methods=['GET'])
@login_required
def myarea():
     match current_user.get_ruolo :
          case 's':
               #Sezione Prenota Esami, non controlla users.c.idutente == current_user.get_id()     
               select(prenotazioni.c.codappello).where(prenotazioni.c.codutente==current_user.get_id())
               pr_es_s1 = conn.execute(select(appelli,prove.c.nome.label('nomeprova'),prove.c.tipo,corsi.c.nome.label('nomecors'),moduli.c.nome.label('nomemod'))\
                    .select_from(join(appelli,join(prove,join(moduli,join(corsiseguiti,corsi)))))\
                    .where(appelli.c.idappello.not_in(select(prenotazioni.c.codappello).where(prenotazioni.c.codutente==current_user.get_id())),corsiseguiti.c.codstudente==current_user.get_id())\
                    .order_by(appelli.c.dataprova)).fetchall()

               # Sezione Visualizzazione prenotazioni
               vis_pre_s1 = conn.execute(select(appelli, prenotazioni.c.idprenotazione,prove,prove.c.nome.label('nomeprova'),prove.c.tipo,corsi.c.nome.label('nomecors'),moduli.c.nome.label('nomemod')).select_from(join(prenotazioni,join(appelli,join(prove,join(moduli,corsi))))).where(prenotazioni.c.codutente == current_user.get_id())).fetchall()
               #filtro li id degli appelli prenotati
               events=[ ap.idappello for ap in vis_pre_s1]
               #ottengo eventuali cambiamenti degli appelli prenotati
               eventss=conn.execute(select(logs).where(logs.c.codappello.in_(events)).order_by(logs.c.timestamp.desc())).fetchall()
               
               #Sezione Corsi seguiti
               lista_es_s1 = conn.execute(select(corsi.c.idcorso, corsi.c.nome).select_from(join(corsi,corsiseguiti)).where(corsiseguiti.c.codstudente == current_user.get_id())).fetchall()

               #Sezione Corsi che puoi seguire
               corsi_da_seguire_j1 = join(users, corsilaurea, users.c.codcorsolaurea == corsilaurea.c.idcorsolaurea)
               corsi_da_seguire_j2 = join(corsi, corsi_da_seguire_j1, corsi.c.codcorsolaurea == corsilaurea.c.idcorsolaurea)

               corsi_da_seguire_s1 = conn.execute(select(corsi.c.nome, corsi.c.idcorso).select_from(corsi_da_seguire_j2).\
                                                  where(and_(users.c.idutente == current_user.get_id(), corsi.c.idcorso.notin_(select(corsiseguiti.c.codcorso).\
                                                  where(users.c.idutente == corsiseguiti.c.codstudente))))).fetchall()
               
               # Sezione Libretto
               libretto_j1 = join(users, corsiseguiti, users.c.idutente == corsiseguiti.c.codstudente)
               libretto_j2 = join(corsi, libretto_j1, corsiseguiti.c.codcorso == corsi.c.idcorso)
               libretto_j4 = outerjoin(libretto_j2,corsisuperati, corsisuperati.c.codcorso == corsi.c.idcorso)

               libertto_s1 = conn.execute(select(corsi.c.nome, corsi.c.cfu, corsisuperati.c.dataregistrazione, corsisuperati.c.voto).select_from(libretto_j4)).fetchall()

               res = make_response(render_template("/myarea/myAreaStud.html", pr_es_s1 = pr_es_s1, vis_pre_s1 = vis_pre_s1, lista_es_s1 = lista_es_s1, corsi_da_seguire_s1 = corsi_da_seguire_s1, libretto_s1 = libertto_s1,e_logs=eventss))

          case 'd':
               #Sezione Modifica appello
               mod1=join(corsi,moduli)
               mod2 = conn.execute(select(prove,moduli.c.nome.label("nomemod"),corsi.c.nome.label("nomecors")).select_from(join(mod1, prove, moduli.c.idmodulo == prove.c.codmodulo)).where(moduli.c.coddocente == current_user.get_id())).fetchall()
               mod3= mod3= conn.execute(select(mod1,corsi).where(moduli.c.coddocente==current_user.get_id())).fetchall()
               corsidoc=[]
               for cors in conn.execute(select(corsi.c.idcorso.distinct(),corsi.c.nome).select_from(join(corsi,moduli)).where(moduli.c.coddocente==current_user.get_id())).fetchall(): #corsi 
                    corss ={}
                    corss["nome"]=cors.nome
                    corss["idcorso"]=cors.idcorso
                    corss["prove"]=[]
                    for mod in conn.execute(select(moduli).where(moduli.c.coddocente==current_user.get_id(),moduli.c.codcorso==cors.idcorso)).fetchall(): # moduli
                         for prova in conn.execute(select(prove).where(prove.c.codmodulo==mod.idmodulo)).fetchall(): # prove
                              corss["prove"].append((prova.nome,prova.idprova,prova.tipo,prova.peso,mod.nome))
                    corsidoc.append(corss)
               
               appelli_q=conn.execute(select(appelli)).fetchall()
               res = make_response(render_template("/myarea/myAreaDoc.html",moddoc=mod3, modify_es = mod2, appellis =appelli_q, cors = corsidoc))
          case 'admin':
               return  redirect(url_for('admin_bp.admin'))
     return res
# [
#      {"nome":nomemod,
#      "prove":[
#           (nomeprova,tipo,peso,idprova,nomemod)
#      ]}
# ]
# ----------------------------------------------------------- docente -------------------------------------------------------------------------
# crezione prova
@myarea_bp.route('/insertprova',methods=['POST'])
@login_required
def insertProva():
     if request.method =='POST':
          try: 
               tipo=request.form['tipo'],
               peso=request.form['peso'],
               nome=request.form['nome'],
               codmodulo = request.form['codmodulo']
               isparziale = request.form.get('isparziale')!=None
               conn.execute(insert(prove).values(
                         tipo = tipo,
                         peso = peso,
                         nome=nome,
                         codmodulo = codmodulo,
                         isparziale=isparziale
                         ))
               get_value = conn.execute(select(prove).where(prove.c.codmodulo==codmodulo)).fetchall()
               tot = 0
               for f in get_value:
                    tot += f.peso

               if(101 > tot):
                    conn.commit()
                    flash('prove_msg: Prova aggiunta con successo','sucess')
               else:
                    flash('prove_msg: Errore nel\' aggiungere la prova, valore superato ','error')
                    conn.rollback()
               
          except:
               flash('prove_msg: Errore nel\' aggiungere la prova','error')
               conn.rollback()
          return redirect(url_for('myarea_bp.myarea'))
     else:
          return abort(403)
# creazione appello
@myarea_bp.route('/insertappello',methods=['POST'])
@login_required
def insertAppello():
     try :
          aula=request.form['aula'],
          ora=request.form['ora'],
          dataprova=request.form['dataProva'],
          datainizioisc=request.form['datainizioisc'],
          datafineisc=request.form['datafineisc'],
          datascadenza=request.form['datascadenza']
          codprova = request.form['codprova']
          conn.execute(insert(appelli).values(
               aula=aula,
               ora = ora,
               dataprova=dataprova,
               datainizioisc = datainizioisc,
               datafineisc=datafineisc,
               datascadenza=datascadenza,
               codprova=codprova
               ))
          conn.commit()
          flash('appelli_msg: Appello aggiunto con successo','success')
     except:
          flash('appelli_msg: Errore nell\' aggiungere l\'appello','error')
          conn.rollback()
     return redirect(url_for('myarea_bp.myarea'))
# Update prova
@myarea_bp.route('/updatees/<int:id>', methods=['POST'])
def updateExam(id):
     if request.method =='POST':
          try:
               tipo=request.form['tipo'],
               peso=request.form['peso'],
               nome=request.form['nome'],
               codmodulo = request.form['codmodulo']
               conn.execute(update(prove).where(prove.c.idprova == id).values(
                              tipo = tipo,
                              peso = peso,
                              nome=nome
                    ))
               get_value = conn.execute(select(prove).where(prove.c.codmodulo==codmodulo)).fetchall()
               tot = 0
               for f in get_value:
                    tot += f.peso
               print(tot)
               if(101 > tot):
                    
                    conn.commit()
                    flash('appelli_msg: Appello aggiunto con successo','success')
               else:
                    flash('prove_msg: Errore nel\' aggiungere la prova, valore superato','error')
                    conn.rollback()
               
          except:
               conn.rollback()
          return redirect(url_for('myarea_bp.myarea'))
     else:
          return abort(403)
# rimozione appello
@myarea_bp.route('/removeAppello/<int:id>', methods=['POST'])
def removeAppello(id):
     conn.execute(delete(appelli).where(appelli.c.idappello == id))
     conn.commit()
     return redirect(url_for('myarea_bp.myarea'))
# rimozione prova
@myarea_bp.route('/removeProva/<int:id>', methods=['POST'])
def removeProva(id):
     conn.execute(delete(prove).where(prove.c.idprova == id))
     conn.commit()
     return redirect(url_for('myarea_bp.myarea'))

# -----------------------------------------------------------  studente -----------------------------------------------------------------------
# iscrizione di un utente ad un appello
@myarea_bp.route('/iscriviappello/<int:id>', methods=['POST'])
@login_required
def insertPrenotazione(id):
     today = date.today()
     conn.execute(insert(prenotazioni).values(
          codutente = current_user.get_id(),
          dataprenotazione = today.strftime("%Y/%m/%d"),
          codappello = id
     ))
     conn.commit()
     return redirect(url_for('myarea_bp.myarea'))
# elimina una prenotazione
@myarea_bp.route('/myareastudrem/<int:id>', methods=['POST'])
@login_required
def deletePrenotazione(id):
     thispreno=conn.execute(select(prenotazioni.c.codutente).where(prenotazioni.c.idprenotazione==id)).fetchone() # controllo che la prenotazione sia dell'utente
     if(int(current_user.get_id())==thispreno.codutente): # controllo che l'utente della prenotazione da cancellare sia l'utente corrente
          conn.execute(delete(prenotazioni).where(prenotazioni.c.idprenotazione == id))
          conn.commit()
          return redirect(url_for('myarea_bp.myarea'))
     else:
          return abort(403)
# Rimuove l'iscrizione del current user ad un corso
@myarea_bp.route('/myareastuddisc/<int:id>', methods=['POST'])
@login_required
def disiscriviCorso(id):
     conn.execute(delete(corsiseguiti).where(corsiseguiti.c.codcorso == id and corsiseguiti.c.codstudente == current_user.get_id()))
     conn.commit()
     return redirect(url_for('myarea_bp.myarea'))
# Iscrive il current user ad un corso
@myarea_bp.route('/myareastudiscr/<int:id>', methods=['POST'])
@login_required
def iscriviCorso(id):
     conn.execute(insert(corsiseguiti).values(
          codcorso = id,
          codstudente = current_user.get_id()
     ))
     conn.commit()
     return redirect(url_for('myarea_bp.myarea'))
