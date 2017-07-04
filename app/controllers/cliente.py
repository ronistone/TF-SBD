from flask import render_template, url_for, abort, session, flash, redirect
from flask_login import current_user, login_required
from app import app,conn
from app.models.decorators import verifica_autorizacao
from app.models.forms import CreateClienteForm
from app.models.tables import Agencia, Funcionario, User
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError


@app.route('/cliente/create',methods=["GET","POST"],endpoint='createCliente')
@login_required
@verifica_autorizacao(1)
def createCliente():
    if not current_user.username in session:
        flash("Cadastre o acesso para o cliente antes de prosseguir!")
        return redirect(url_for('register',path='cliente'))
    else:
        sessao = session[current_user.username]
    form = CreateClienteForm()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    cursor.execute("SELECT * FROM funcionario")
    di = cursor.fetchall()
    funcionario = []
    access = ["Cliente","Funcionário","Gerente","Administrador"]
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        funcionario += [Funcionario(d).getChoice()]
    form.gerente.choices = funcionario
    if form.validate_on_submit():
        try:
            user = User(sessao)
            user.generate_password()
            cursor.execute("""INSERT INTO users(username,password)
                            VALUES('%s','%s')""" % (user.username,user.password))
            cursor.execute("SELECT id FROM users WHERE username = '%s'"%(user.username))
            di = cursor.fetchone()
            cursor.execute("""INSERT INTO
                            cliente(id,nome,cpf,data_nasc,endereco,cidade,estado,telefone,id_gerente)
                            VALUES
                            ('%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (di[0],form.nome.data,form.cpf.data,form.data_nasc.data,
                            form.endereco.data,form.city.data,form.state.data,form.telefone.data,form.gerente.data))
            conn.commit()
            session.pop(current_user.username,None)
            flash("Cliente Criado!")
            return redirect(url_for('dashboard'))
        except IntegrityError as error:
            if error.pgcode == '23505':
                flash('Usuário já utilizado')
            conn.rollback()
            return redirect(url_for('register',path='cliente'))
        except Exception as error:
            print(error)
            conn.rollback()
            flash('Desculpe, tivemos um problema. Tente novamente!')
            return redirect(url_for('register',path='cliente'))
    return render_template('createCliente.html', access=access[int(sessao['level'])],form=form,sessao=sessao)


@app.route('/example')
def example():
    return render_template('forms.html')