from esami import *
from flask_login import *
from model import *
from myarea import *
from datetime import date
import traceback

@login_required
def isTeacherMod(id):
    modteacher =conn.execute(select(moduli.c.coddocente).select_from(join(appelli,join(prove,moduli))).where(appelli.c.idappello==id)).fetchone()
    return current_user.get_ruolo =='d' and int(current_user.get_id()) ==modteacher.coddocente


@esami_bp.route('/appelli/<int:id>')
def addVoto(id):
    if isTeacherMod(id):
        current_app = conn.execute(select(corsi.c.nome.label('nomecors'), moduli.c.nome.label('nomemod'),appelli,prove).select_from(join(appelli,join(prove,join(moduli,corsi)))).where(appelli.c.idappello==id)).fetchone()
        reg_stud_q = select(join(users,proveregistrate,users.c.idutente==proveregistrate.c.codstudente)).where(proveregistrate.c.codappello==id)
        registeredstudents=conn.execute(reg_stud_q).fetchall()
        # utenti che non hanno una prova registrata e hanno una prenotazione in quell'appello
        not_reg = conn.execute(select(users).where(users.c.idutente.not_in(select(proveregistrate.c.codstudente).where(proveregistrate.c.codappello==id)),users.c.idutente.in_(select(prenotazioni.c.codutente).where(prenotazioni.c.codappello==id)))).fetchall()
        return render_template("/esami/voto.html", es = not_reg,allstu = registeredstudents, appp=current_app)
    else:
        abort(403)

@esami_bp.route('/updateappello/<int:id>',methods=['POST'])
@login_required
def updateAppello(id):
    if  isTeacherMod(id):
        try:
            dataapp = request.form['dataprova']
            datainizio = request.form['datainizioisc']
            datafine = request.form['datafineisc']
            datascad = request.form['datascadenza']
            orario = request.form['ora']
            aula = request.form['aula']
            conn.execute(
                update(appelli).where(appelli.c.idappello==id).values(
                    dataprova=dataapp,
                    datainizioisc=datainizio,
                    datafineisc=datafine,
                    datascadenza=datascad,
                    aula=aula,
                    ora=orario,
                )
            )
            conn.commit()
        except Exception as error:
            conn.rollback()
        return redirect(url_for('esami_bp.addVoto',id=id))
    else:
        abort(403)

@esami_bp.route('/confirmes/<int:ida>', methods=['POST'])
@login_required
def confirmVoto(ida):
    if isTeacherMod(ida):
        try : 
            today = date.today()
            codstudente = request.form['codstudente'],
            voto = request.form['voto']
            conn.execute(insert(proveregistrate).values(
                codstudente = codstudente,
                codappello = ida,
                coddocente = current_user.get_id(),
                voto = voto,
                dataregistrazione = today.strftime("%Y/%m/%d"),
            ))
            conn.commit()
        except:
            conn.rollback()
        return redirect(url_for('esami_bp.addVoto',id=ida))
    else:
        return abort(403)

@esami_bp.route('/deletes/<int:id>', methods=['POST'])
@login_required
def deletevoto(id):
    if isTeacherMod(id):
        try:
            conn.execute(delete(proveregistrate).where(proveregistrate.c.idprovaregistrata==id))
            conn.commit()
        except:
            conn.rollback()
        return redirect(url_for('esami_bp.addVoto',id=request.form['appello']))
    else:
        return abort(403)

@esami_bp.route('/deleteappello/<int:id>', methods=['POST'])
@login_required
def deleteappello(id):
    if isTeacherMod(id):
        try:
            conn.execute(delete(appelli).where(appelli.c.idappello ==id))
            conn.commit()
        except:
            conn.rollback()
        return redirect(url_for('myarea_bp.myarea'))
    else:
        return abort(403)

@esami_bp.route('/appelli/<int:idapp>/users')
def userslist(idapp):
    # if isTeacherMod(idapp):
    users_list = conn.execute(select(join(proveregistrate,users,users.c.idutente == proveregistrate.c.codstudente)).where(proveregistrate.c.codappello==idapp)).fetchall()
    return render_template('/esami/users.html',all_us=users_list)
    # else:
    #     abort(403)

