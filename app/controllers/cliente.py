from flask import render_template, url_for, abort
from flask_login import current_user, login_user
from app import app,conn
from app.models.decorators import verifica_autorizacao
from psycopg2.extras import DictCursor


@app.route('/cliente/create',methods=["GET","POST"],endpoint='createCliente')
@login_required
@verifica_autorizacao(1)
def createCliente():
    pass