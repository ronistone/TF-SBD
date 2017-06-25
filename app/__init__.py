from flask import Flask
from flask_login import LoginManager
from psycopg2.extras import DictCursor
import psycopg2
import os

app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)

conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s port=%s" %(app.config['DB_HOST'],app.config['DB_NAME'],
                                                                        app.config['DB_USER'],app.config['DB_PASSWORD'],
                                                                        app.config['DB_PORT']))
print('Connection Open')



from app.controllers import default,agencia
from app.models import tables

@app.cli.command()
def initdb():
    cursor = conn.cursor(cursor_factory=DictCursor)
    fopen= open('db.sql','r')
    script = fopen.read()
    fopen.close()

    sqlcommands = script.split(';')
    for command in sqlcommands[0:len(sqlcommands)-1]:
        try:
            cursor.execute(command+';')
        except Exception as msg:
            print("Erro: ",msg)

    cursor.execute("SELECT * FROM users")
    usuario = cursor.fetchall()
    for u in usuario:
        user = tables.User(u)
        user.generate_password()
        cursor.execute("UPDATE users SET password = '"+user.password+"';")
        conn.commit()
    print("Tudo Pronto!")


import signal
import sys
def signal_handler(signal, frame):
        conn.close()
        print("Connection Close!")
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)