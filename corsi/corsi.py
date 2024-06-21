from corsi import *
from flask import abort,request
from datetime import date

@corsi_bp.route('/')
def corsiall():
    # seleziona corsi 
    allcours=conn.execute(select(join(corsi,corsilaurea)).select_from(join(corsi,corsilaurea))).fetchall()
    return render_template("/corsi/corsi.html",courses=allcours)

@corsi_bp.route('/corso/<int:id>')
def corsoone(id):
    #selezioni i corsi del corso di laurea
    corsores = conn.execute(select(corsi).where(corsi.c.idcorso==id)).fetchone()._asdict()
    if(corsores is None):
        abort(404)
    #seleziono i moduli ed i relativi docenti
    moduli_q = join(users,moduli, users.c.idutente == moduli.c.coddocente )
    modulis = conn.execute(select(users.c.nome,users.c.cognome,moduli.c.nome,moduli.c.idmodulo).select_from(moduli_q).where(moduli.c.codcorso == corsores['idcorso'] and (moduli.c.coddocente ==users.c.idutente))).fetchall()
    #seleziono gli appelli disponibili
    appelli_q =conn.execute(select(join(moduli,join(prove,appelli))).where(moduli.c.codcorso==id)).fetchall()
    prenota = conn.execute(select(prenotazioni.c.codappello).where(prenotazioni.c.codutente==current_user.get_id())).fetchall()
    results = [r for (r, ) in prenota]
    return render_template("/corsi/corso.html",corso=corsores,modul=modulis,appelli=appelli_q,pren = results)

# Iscrive l'utente ad un appello
@corsi_bp.route('/addprova/<idcorso>',methods=['POST'])
@login_required
def insertprova(idcorso):
    try:
        userid= current_user.get_id()
        today = date.today()
        conn.execute(insert(prenotazioni).values(
        codappello=request.form['idappello'],
        codutente = userid,
        dataprenotazione = today.strftime("%Y/%m/%d")
        ))
        conn.commit()
    except:
        conn.rollback()
    return redirect(url_for('corsi_bp.corsoone',id=idcorso))

# rimuove l'iscrizione da un appello
@corsi_bp.route('/removeprova/<idcorso>',methods=['POST'])
@login_required
def deleteprova(idcorso):
    try:
        conn.execute(delete(prenotazioni).where(prenotazioni.c.codappello==request.form['codappello'] and (prenotazioni.c.codutente==current_user.get_id())))
        conn.commit()
    except:
        conn.rollback()
    return redirect(url_for('corsi_bp.corsoone',id=idcorso))
