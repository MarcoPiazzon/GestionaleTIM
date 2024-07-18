from flask import Blueprint,render_template,request,redirect,url_for
from sqlalchemy import *
from login import login_bpp
from flask_login import *
from model import *
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt()
import pandas as pd


@login_bpp.route('/',methods=['POST','GET'])
def login():
    
    if request.method=='POST':
        pw=conn.execute(select(utente).where(utente.c.email==request.form['email'])).fetchone()
        print(pw)
        if(pw is not None): # ha trovato un match sul db -> utente da autenticare
            pw = pw._asdict()
            if(bcrypt.check_password_hash(pw['psw'],pw['email']+request.form['psw'])):
                login_user(User(pw['idutente'],pw['email'])) # utilizzo flask_login per creare i cookies
                return redirect(url_for('portafoglio_bp.home', idPort=current_user.idPort, id=0))
            return render_template("/login/login.html",err=2) # wrong password
        return render_template("/login/login.html",err=1) # wrong email
    else :
        if  current_user.is_authenticated : # se l'utente è già autenticato allora lo reindirizzo nell'area riservata
            return redirect(url_for('home_bp.home'))
        return render_template("/login/login.html",err=0)

@login_bpp.route('/logout')
def logoutuser():
    logout_user()
    return render_template("/login/login.html",err=0)