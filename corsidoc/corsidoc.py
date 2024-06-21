from flask import abort,request
from flask_login import *
from datetime import date
from corsidoc import *
import math

# funzione che ritorna true se il current user è docente di qualsiasi modulo del corso passato come parametro
@login_required
def isTeacherCourse(idCorso):
    return int(current_user.get_id()) in [doc for (doc, ) in conn.execute(select(moduli.c.coddocente).select_from(join(moduli,corsi)).where(corsi.c.idcorso==idCorso)).fetchall()]

@corsidoc_bp.route('/corso/<int:id>')
@login_required
def corsidoc(id):
    if current_user.get_ruolo == 'd' and isTeacherCourse(id):
        studcorso=conn.execute(select(join(users,corsiseguiti)).where(corsiseguiti.c.codcorso==id)).fetchall()
        mods=conn.execute(select(moduli).where(moduli.c.codcorso==id)).fetchall()
        all_studs=[]
        for stud in studcorso:
            stdinfo ={}
            stdinfo["idstudente"]=stud.idutente
            stdinfo["nome_cogn"]=stud.nome+" "+stud.cognome
            stdinfo["email"]=stud.email
            stdinfo["moduli"]={}
            stdinfo["votofinale"]=0
            stdinfo["passed"]=True 
            for mod in mods: # scorro per ogni modulo del corso
                stdinfo["moduli"][mod.nome]={}
                stdinfo["moduli"][mod.nome]["idmod"]=mod.idmodulo
                stdinfo["moduli"][mod.nome]["voto"]=0
                stdinfo["moduli"][mod.nome]["passed"]=True
                stdinfo["moduli"][mod.nome]["prove"]=[]
                for prova in conn.execute(select(prove).where(prove.c.codmodulo==mod.idmodulo)).fetchall(): # scorro per ogni prova del modulo
                    provaa={}
                    provaa["appelli"]=[] # lista di tentativi della prova
                    provaa["nome"]=prova.nome
                    provaa["idprova"]=prova.idprova
                    provaa["tipo"]=prova.tipo
                    provaa["voto"]=0
                    provaa["isparziale"]=prova.isparziale
                    provaa["peso"]=prova.peso
                    for appello in conn.execute(select(appelli).where(appelli.c.codprova==prova.idprova)).fetchall(): # fetcho gli appelli della prova
                        for proreg in conn.execute(select(proveregistrate,appelli,prove).select_from(join(proveregistrate,join(appelli,prove))).where(proveregistrate.c.codappello==appello.idappello,proveregistrate.c.codstudente==stud.idutente).order_by(proveregistrate.c.dataregistrazione.asc())).fetchall(): # fetch le prove registrate per ogni appello 
                            votoo =(proreg.voto,proreg.dataprova,proreg.datascadenza)
                            provaa["appelli"].append(votoo)
                    if len(provaa["appelli"])!= 0: # controlla se ci sono prove registrate 
                        valid =provaa["appelli"][0][0]>=18 and provaa["appelli"][0][2]>date.today() 
                        provaa["voto"]=provaa["appelli"][0][0] # assegno il voto finale della prova all'ultimo appello dato in base alla data di registrazione del voto
                        stdinfo["moduli"][mod.nome]["prove"].append(provaa)
                        stdinfo["moduli"][mod.nome]["voto"]+=provaa["voto"]*provaa["peso"]/100 # calcolo il voto finale del modulo = la somma del voto di ogni prova per il suo peso
                        if valid : # se l'ultimo appello dato è >18 allora la prova è considerata passata (in generale bisogna sempre passare con 18 i parziali) e non è scaduto
                            if not provaa["isparziale"]: # se l'ultimo appello tentato è un completo allora non mi serve controllare altre prove
                                stdinfo["moduli"][mod.nome]["passed"]=True
                                break
                            else:
                                stdinfo["moduli"][mod.nome]["passed"]= valid and stdinfo["moduli"][mod.nome]["passed"]
                        else: # c'è una prova ma non è valida
                            stdinfo["moduli"][mod.nome]["passed"]=False
                    else: # non ci sono prove registrate nel modulo
                            stdinfo["moduli"][mod.nome]["passed"]=False
                                
                stdinfo["votofinale"]+=math.ceil((stdinfo["moduli"][mod.nome]["voto"]))
                stdinfo["passed"]=stdinfo["passed"] and stdinfo["moduli"][mod.nome]["passed"]
            all_studs.append(stdinfo)
        pass_stud=conn.execute(select(users.c.idutente).select_from(join(users,corsisuperati)).where(corsisuperati.c.codcorso==id)).fetchall()
        print(all_studs)
        return render_template('/corsidoc/corso.html',all_studs=all_studs,pass_stu= pass_stud)
    else :
        abort(403)

    # {
    #     "idstudente": int,
    #     "nome_cogn": string,
    #     "email": string,
    #     "moduli":{
    #         "modulo1":{
    #             "imod": int,
    #             "passed": boolean,
    #             "voto": float
    #             "prove":[
    #                   { "nome":string,
    #                     "idprova":int
    #                     "tipo":string
    #                     "voto":int
    #                     "isparziale":boolean
    #                     "peso":int
    #                     "appelli":[ (voto,datascadenza,dataprova)]
    #                       }
    #              ]
    #         }
    #     }
    #     "votofinale": int,
    #     "passed": boolean,
    # }

@corsidoc_bp.route('/confirm/<int:id>', methods=['POST'])
@login_required
def confirm(id):
    if current_user.get_ruolo == 'd' and isTeacherCourse(id):
        try:
            voto=request.form['voto']
            corso=request.form['corso']
            stud=id
            conn.execute(insert(corsisuperati).values(
                dataregistrazione=date.today(),
                codcorso=corso,
                codstudente=stud,
                voto=voto
            ))
            conn.commit()
        except:
            conn.rollback()
        return redirect(url_for(corsidoc_bp.corsi,id=corso))
    else :
        abort(403)