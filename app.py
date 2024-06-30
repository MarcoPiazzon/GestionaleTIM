from sqlalchemy import *
from flask_login import *
from flask import Flask,redirect,url_for,render_template,make_response, request
from home.home import home_bp
from myarea.myarea import myarea_bp
from login.login import login_bpp
from corsi.corsi import corsi_bp
from admin.admin import admin_bp
from corsilaurea.corsilaurea import corsilaurea_bp
from esami.esami import esami_bp
from corsidoc.corsidoc import corsidoc_bp
from portafoglio.portafoglio import portafoglio_bp 
from calendario.calendario import calendario_bp
from contatto.contatto import contatto_bp
from model import *
import datetime
import pandas
import openpyxl
app=Flask(__name__)
app.config['SECRET_KEY']='asd'

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = conn.execute(select(utente).where(utente.c.idUtente==user_id)).fetchone()._asdict()
    return User(user_id,user['email'])

@app.context_processor
def inject_today_date():
    return {'today_date': datetime.date.today()}

app.register_blueprint(login_bpp,url_prefix='/login')
app.register_blueprint(home_bp,url_prefix='/home')
app.register_blueprint(myarea_bp,url_prefix='/myarea')
app.register_blueprint(corsi_bp,url_prefix='/corsi')
app.register_blueprint(admin_bp,url_prefix='/admin')
app.register_blueprint(corsilaurea_bp,url_prefix='/corsilaurea')
app.register_blueprint(esami_bp,url_prefix='/esami')
app.register_blueprint(corsidoc_bp,url_prefix='/corsidoc')
app.register_blueprint(portafoglio_bp, url_prefix='/portafoglio')
app.register_blueprint(calendario_bp, url_prefix='/calendario')
app.register_blueprint(contatto_bp, url_prefix='/contatto')

@app.route('/')
def main():
    return redirect(url_for('portafoglio_bp.home', idPort=current_user.idPort, id=0))
    

@app.errorhandler(500)    
def error_handler(error):
        return render_template("/errors/500.html")

@app.errorhandler(404)
def error_handler(error):
    return render_template("/errors/404.html")

@app.errorhandler(401)
def error_handler(error):
    return render_template("/errors/401.html")
    
@app.errorhandler(403)
def error_handler(error):
    return render_template("/errors/403.html")

@login_required
@app.route('/appelli/<int:idapp>/users/download',methods=['POST'])
def userslistds(idapp):
    with app.test_client() as client:
        res =client.get('/esami/appelli/'+str(idapp)+'/users')
        content=res.data.decode('utf-8')
    pdf = HTML(string=content).write_pdf()
    respo= make_response(pdf)
    respo.headers['Content-Type'] = 'application/pdf'
    respo.headers['Content-Disposition'] = 'attachment; filename=risultati.pdf'
    return respo

app.run(debug=True)