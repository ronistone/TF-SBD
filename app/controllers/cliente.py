from flask import render_template, url_for, abort, session, flash, redirect, request
from flask_login import current_user, login_required
from app import app,conn
from app.models.decorators import verifica_autorizacao,verifica_autorizacao_or_is_user, verifica_autorizacao_num
from app.models.forms import CreateClienteForm, EditClienteForm
from app.models.tables import Agencia, Funcionario, User, Cliente
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
    cursor.execute("SELECT * FROM funcionario INNER JOIN users ON id = num_func")
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
            cursor.execute("""INSERT INTO users(username,password,nome,telefone)
                            VALUES('%s','%s','%s','%s')""" % (user.username,user.password,form.nome.data,form.telefone.data))
            cursor.execute("SELECT id FROM users WHERE username = '%s'"%(user.username))
            di = cursor.fetchone()
            cursor.execute("""INSERT INTO
                            cliente(id,cpf,data_nasc,endereco,cidade,estado,id_gerente)
                            VALUES
                            ('%s','%s','%s','%s','%s','%s','%s')""" % (di[0],form.cpf.data,form.data_nasc.data,
                            form.endereco.data,form.city.data,form.state.data,form.gerente.data))
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


@app.route('/cliente/get', endpoint='getCliente')
@login_required
@verifica_autorizacao(1)
def getCliente():
    ger = request.args.get('ger')
    agencia = None
    if ger == "-1":
        agencia = request.args.get('agencia')
        if not agencia:
            return redirect(url_for('getAgencia',opcao='cliente'))
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("SET search_path TO agencia")
        if ger == "-1":
            cursor.execute("""SELECT u1.*,u2.nome AS gerente, cliente.* FROM (cliente INNER JOIN users AS u1 ON cliente.id = u1.id) INNER JOIN (funcionario INNER JOIN users AS u2 ON funcionario.num_func = u2.id) ON cliente.id_gerente = funcionario.num_func WHERE nome_ag = '%s' """ %(agencia))
        else:
            cursor.execute("""SELECT u1.*,u2.nome AS gerente, cliente.* FROM (cliente INNER JOIN users AS u1 ON cliente.id = u1.id) INNER JOIN (funcionario INNER JOIN users AS u2 ON funcionario.num_func = u2.id) ON cliente.id_gerente = funcionario.num_func WHERE id_gerente = '%s' """ %(ger))
        di = cursor.fetchall()
        clientes = []
        access = ["Cliente","Funcionário","Gerente","Administrador"]
        for i in range(0,len(di)):
            d = {}
            for key,value in di[i]._index.items():
                d[key] = di[i][value]
            clientes += [Cliente(d)]
        return render_template('getCliente.html',clientes=clientes,access=access)
    except Exception as error:
        conn.rollback()
        print(error)
        flash("DEU RUIM!")
        return redirect('dashboard')

@app.route('/cliente/edit/<int:num_func>',methods=["GET","POST"], endpoint='editCliente')
@login_required
@verifica_autorizacao_or_is_user(2)
def editCliente(num_func):
    form = EditClienteForm()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    access = ["Cliente","Funcionário","Gerente","Administrador"]

    ###########  Pegando Gerentes para o form ################
    cursor.execute("SELECT * FROM funcionario INNER JOIN users ON num_func = id")
    di = cursor.fetchall()
    gerentes = []
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        gerentes += [Funcionario(d).getChoice()]
    form.id_gerente.choices = gerentes
    ###########################################################
    cursor.execute("""SELECT * FROM users
                    INNER JOIN cliente ON users.id = cliente.id
                    WHERE cliente.id = '%s'""" %(num_func))
    di = cursor.fetchone()
    user = {}
    for key,value in di._index.items():
        user[key] = di[value]
    user = User(user)
    if form.validate_on_submit():
        if not current_user.check_password(form.youpassword.data):
            flash("Sua senha é Inválida!")
            return redirect(url_for('editCliente',num_func=num_func))

        try:
            func = ["cpf","data_nasc","endereco","cidade","estado","id_gerente"]
            us = ["password","telefone","nome"]
            insert = ""
            for key,value in form.data.items():
                if key in func and (type(value) is str and len(value) > 1 or type(value) != str):
                    insert += "%s = '%s',"%(key,value)

            cursor.execute("""UPDATE cliente
                            SET %s
                            WHERE id = %r""" %(insert[0:len(insert)-1],num_func))

            u = User({'password':form.password.data})
            if form.password.data is "":
                u.password = user.password
            else:
                u.generate_password()

            cursor.execute("""UPDATE users
                            SET password = '%s'
                            WHERE id = '%s'""" %(u.password,num_func))
            conn.commit()
            flash("Usuário atualizado")
            return redirect(url_for('editCliente',num_func=num_func))
        except Exception as error:
            print(error)
            conn.rollback()
    form.id_gerente.data = str(user.id_gerente)
    return render_template('editCliente.html',form=form,user=user)


@app.route('/cliente/edit/<int:num_func>', endpoint='deleteCliente')
@login_required
@verifica_autorizacao_num(2)
def deleteCliente(num_func):
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    try:
        cursor.execute("DELETE FROM cliente WHERE id= %s"%(num_func))
        cursor.execute("DELETE FROM users WHERE id= %s"%(num_func))
        conn.commit()
        flash("O Cliente foi excluido")
        return redirect(url_for('getCliente'))
    except Exception as error:
        flash("Tivemos um problema, tente novamente!")
        return redirect(url_for('getCliente '))
