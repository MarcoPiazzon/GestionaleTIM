import string
from sqlalchemy import *
from flask_login import *
import os
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(os.getenv('DB_LINK'),future=True)
metadata=MetaData()
conn=engine.connect()

andamentotrattativa = Table('andamentotrattativa',metadata, autoload_with=engine) 
appuntamento = Table('appuntamento',metadata, autoload_with=engine)
categoria = Table('categoria',metadata, autoload_with=engine)
cliente = Table('cliente',metadata, autoload_with=engine)
clienteappuntamento = Table('clienteappuntamento',metadata, autoload_with=engine)
comune = Table('comune',metadata, autoload_with=engine)
contatto = Table('contatto',metadata, autoload_with=engine)
partecipanti = Table('partecipanti',metadata, autoload_with=engine)
portafoglio = Table('portafoglio',metadata, autoload_with=engine)
presidio = Table('presidio',metadata, autoload_with=engine)
#regione = Table('regione',metadata, autoload_with=engine)
tipocliente = Table('tipocliente',metadata, autoload_with=engine)
trattativa = Table('trattativa',metadata, autoload_with=engine)
trattativaappuntamento = Table('trattativaappuntamento',metadata, autoload_with=engine)
utente = Table('utente',metadata, autoload_with=engine)
utentehacontatto = Table('utentehacontatto',metadata, autoload_with=engine)

class User(UserMixin):
    
    def __init__(self,id,email) -> None:
        self.id=id
        self.email=email
        res =conn.execute(select(utente).where(utente.c.email==email)).fetchone()._asdict()
        self.nome = res['nome']
        self.cognome = res['cognome']
    @property
    def getnames(self) -> string:
        return self.nome +" "+self.cognome
