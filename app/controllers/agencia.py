from flask import render_template,redirect,url_for
from flask_login import login_user,logout_user, login_required, current_user
from app import app,lm,conn
from app.models.tables import User
from app.models.forms import LoginForm,CreateAgenciaForm
from psycopg2.extras import DictCursor
from app.models.decorators import verifica_autorizacao
import psycopg2



@app.route('/agencia/create',methods=["GET","POST"],endpoint='criaAgencia')
@login_required
@verifica_autorizacao(3)
def criaAgencia():
    form = CreateAgenciaForm()
    cursor = conn.cursor(cursor_factory=DictCursor)
    if form.validate_on_submit():
        print(form.city.data)
        print(form.state.data)
        cursor.execute("INSERT INTO agencia(nome,cidade,estado) VALUES('"+
                        form.name.data+"','"+form.city.data+"','"+form.state.data+"');")
        conn.commit()
        return redirect(url_for('dashboard'))
    return render_template('agenciaCreate.html',form=form)
@app.route('/agencia/')



@app.route('/example',endpoint='example')
def exemple():
    return render_template('cidades.html')