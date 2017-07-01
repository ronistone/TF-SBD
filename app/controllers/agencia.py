from flask import render_template,redirect,url_for, request, flash,abort
from flask_login import login_required
from app import app,conn
from app.models.tables import Agencia
from app.models.forms import CreateAgenciaForm, GetAgenciaForm, EditAgenciaForm
from app.models.decorators import verifica_autorizacao, verifica_autorizacao_agencia
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError

@app.route('/agencia/create',methods=["GET","POST"],endpoint='criaAgencia')
@login_required
@verifica_autorizacao(3)
def criaAgencia():
    form = CreateAgenciaForm()
    cursor = conn.cursor(cursor_factory=DictCursor)
    if form.validate_on_submit():
        cursor.execute("INSERT INTO agencia(nome,cidade,estado) VALUES('"+
                        form.name.data+"','"+form.city.data+"','"+form.state.data+"');")
        conn.commit()
        return redirect(url_for('dashboard'))
    return render_template('agenciaCreate.html',form=form)

@app.route('/agencia/get',methods=["GET","POST"], endpoint='getAgencia')
@login_required
@verifica_autorizacao(3)
def getAgencia():
    form = GetAgenciaForm()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    cursor.execute("SELECT * FROM agencia")
    di = cursor.fetchall()
    agencia = []
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        agencia += [Agencia(d).getChoice()]
    form.agencia.choices = agencia
    if form.validate_on_submit():
        opcao = request.args.get('opcao')
        if opcao == 'edit':
            return redirect(url_for('editAgencia',agencia=form.agencia.data))
        elif opcao == 'delete':
            return redirect(url_for('deleteAgencia',agencia=form.agencia.data))
        else:
            flash("Ocorreu um problema!")
    return render_template('getAgencia.html', form = form)


@app.route('/agencia/edit',endpoint='editAgencia',methods=["GET","POST"])
@login_required
@verifica_autorizacao_agencia(3)
def editAgencia(agencia):
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    cursor.execute("SELECT * FROM agencia WHERE  nome = '%s'" %(agencia))
    di = cursor.fetchone()
    d = {}
    for key,value in di._index.items():
        d[key] = di[value]
    data = Agencia(d)
    form = EditAgenciaForm()
    if form.validate_on_submit():
        cursor.execute("UPDATE agencia set nome = '%s', cidade = '%s', estado = '%s' WHERE nome = '%s';" %(form.nome.data,form.cidade.data,form.estado.data,data.nome))
        conn.commit()
        return redirect(url_for('editAgencia',agencia=form.nome.data))
    return render_template('editAgencia.html',agencia=data,form=form)

@app.route('/agencia/delete',endpoint='deleteAgencia',methods=["GET","POST"])
@login_required
@verifica_autorizacao_agencia(3)
def deleteAgencia(agencia):
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    cursor.execute("SELECT * FROM agencia WHERE  nome = '%s'" %(agencia))
    di = cursor.fetchone()
    d = {}
    for key,value in di._index.items():
        d[key] = di[value]
    data = Agencia(d)
    try:
        cursor.execute("DELETE FROM agencia WHERE nome = '%s';" %(data.nome))
        conn.commit()
        return redirect(url_for('getAgencia'))
    except IntegrityError as error:
        conn.rollback()
        return render_template("deleteAgencia.html")
    except Exception as error:
        print(error)
        abort(500)