from os import abort
import traceback
from flask import request
from admin import *
from login.login import bcrypt
@admin_bp.route('/')
@login_required
def admin():
    if current_user.get_ruolo =='admin':
        # Seleziona tutti gli utenti e, se studenti, il loro corso di laurea
        us = conn.execute(select(outerjoin(users,corsilaurea))).fetchall()
        # Selezione informazioni relative a tutti i corsi di laurea
        corsilaurea_q= conn.execute(select(corsilaurea)).fetchall()
        # Selezione informazioni di ogni corso
        corsi_q= conn.execute(select(join(corsi,corsilaurea,corsi.c.codcorsolaurea==corsilaurea.c.idcorsolaurea))).fetchall()
        # Seleziona informazioni di ogni modulo
        moduli_q= conn.execute(select(join(users,join(moduli,corsi)),users.c.nome.label('nomedoc'),moduli.c.nome.label("nomemod"),corsi.c.nome.label("nomecor"))).fetchall()
        return render_template("/admin/admin.html",all_users=us,all_corsil=corsilaurea_q,all_corsi=corsi_q,all_moduli=moduli_q)
    else :
        return abort(403)

@admin_bp.route('/insertuser',methods=['POST'])
@login_required
def insertuser():
    if current_user.get_ruolo =='admin':
        # Creazione di un utente
        try:
            ruolo=request.form['ruolo'],
            nome=request.form['nome'],
            cognome=request.form['cognome'],
            telefono=request.form['telefono'],
            password=bcrypt.generate_password_hash(request.form['email']+request.form['password']).decode('utf-8'),
            email=request.form['email'],
            dataiscrizione=request.form['data']
            conn.execute(insert(users).values(
                ruolo = ruolo,
                nome = nome,
                cognome=cognome,
                telefono=telefono,
                password=password,
                email=email,
                dataiscrizione=dataiscrizione
                ))
            conn.commit()
        except:
                conn.rollback()
    return redirect(url_for('admin_bp.admin'))

        
@admin_bp.route('/insertcorsol',methods=['POST'])
@login_required
def insertcorsol():
    if current_user.get_ruolo =='admin':
        # inserimento corso di laurea
        try: 
            nome=request.form['nome'],
            annoaccademico=request.form['annoaccademico']
            conn.execute(insert(corsilaurea).values(
                nome = nome,
                annoaccademico=annoaccademico
                ))
            conn.commit()
        except:
            conn.rollback()
    return redirect(url_for('admin_bp.admin'))

@admin_bp.route('/insertcorso',methods=['POST'])
@login_required
def insertcorso():
    if current_user.get_ruolo =='admin':
        # inserimento corso
        try: 
            nome=request.form['nome'],
            codcorsolaurea=request.form['codcorsolaurea']
            cfu=request.form['cfu']
            conn.execute(insert(corsi).values(
                nome = nome,
                codcorsolaurea=codcorsolaurea,
                cfu=cfu
                ))
            conn.commit()
        except Exception as error:
            conn.rollback()
    return redirect(url_for('admin_bp.admin'))

@admin_bp.route('/insertmodulo',methods=['POST'])
@login_required
def insertmodulo():
    if current_user.get_ruolo =='admin':
        # inserimento modulo
        try:
            nome=request.form['nome'],
            coddocente=request.form['coddocente']
            codcorso=request.form['codcorso']
            conn.execute(insert(moduli).values(
                nome = nome,
                coddocente=coddocente,
                codcorso=codcorso
                ))
            conn.commit()
        except Exception as error:
            print(traceback.format_exc())
            conn.rollback()
    return redirect(url_for('admin_bp.admin'))

