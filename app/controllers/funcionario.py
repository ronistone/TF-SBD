from flask import render_template, url_for, flash, abort, redirect, session
from flask_login import login_required,current_user
from app.models.tables import Funcionario, Agencia, User
from app.models.decorators import verifica_autorizacao, destroy_session_argument
from app.models.forms import CreateFuncionarioForm
from app import conn,app
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError

@app.route('/funcionario/create',methods=["GET","POST"],endpoint='createFuncionario')
@login_required
@verifica_autorizacao(2)
def createFuncionario():
    if not current_user.username in session:
        flash("Cadastre o acesso para o funcionario antes de prosseguir!")
        return redirect(url_for('register',path='funcionario'))
    else:
        sessao = session[current_user.username]
    form = CreateFuncionarioForm()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    cursor.execute("SELECT * FROM agencia")
    di = cursor.fetchall()
    agencia = []
    access = ["Cliente","Funcionário","Gerente","Administrador"]
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        agencia += [Agencia(d).getChoice()]
    form.agencia.choices = agencia
    if form.validate_on_submit():
        try:
            user = User(sessao)
            user.generate_password()
            cursor.execute("INSERT INTO users(username,password,level,is_func) VALUES('%s','%s','%s','TRUE')" % (user.username,user.password,user.level))
            cursor.execute("SELECT MAX(id) FROM users")
            di = cursor.fetchone()
            cursor.execute("INSERT INTO funcionario(nome,telefone,id_user,nome_ag) VALUES('%s','%s','%s','%s')" % (form.name.data,form.phone.data,di[0],form.agencia.data))
            conn.commit()
            session.pop(current_user.username,None)
            flash("Funcionario Criado!")
            return redirect(url_for('dashboard'))
        except IntegrityError as error:
            if error.pgcode == '23505':
                flash('Usuario ja utilizado')
            conn.rollback()
            return redirect(url_for('register',path='funcionario'))
        except Exception as error:
            conn.rollback()
            flash('Desculpe, tivemos um problema. Tente novamente!')
            return redirect(url_for('register',path='funcionario'))
    return render_template('createFuncionario.html', access=access[int(sessao['level'])],form=form,sessao=sessao)


@app.route("/funcionario/get")
@login_required
@verifica_autorizacao(2)
def getFuncionario():
    pass