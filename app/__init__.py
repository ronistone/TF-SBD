from flask import Flask
from flask_login import LoginManager
from flask_script import Manager
from psycopg2.extras import DictCursor
import psycopg2
import os
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


app = Flask(__name__)
app.config.from_object('config')
manager = Manager(app)
lm = LoginManager()
lm.init_app(app)

conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s port=%s" %(app.config['DB_HOST'],app.config['DB_NAME'],
                                                                        app.config['DB_USER'],app.config['DB_PASSWORD'],
                                                                        app.config['DB_PORT']))
print('Conexão Aberta!')



from app.controllers import default, agencia, funcionario, cliente, conta
from app.models import tables

@manager.command
def initdb():
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(open("db.sql","r").read())
        conn.commit()
        #############   Criptografando senhas   ###############
        cursor.execute("SELECT * FROM users")
        usuario = cursor.fetchall()
        for u in usuario:
            user = tables.User(u)
            user.generate_password()
            cursor.execute("UPDATE users SET password = '%s'"%(user.password))
            conn.commit()
        ########################################################
        conn.close()
    except Exception as error:
        print(error)
    print("Conexão Fechada!")
    print("Tudo Pronto!")


import signal
import sys
def signal_handler(signal, frame):
        conn.close()
        print("Conexão Fechada!")
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)