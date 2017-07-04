from flask import render_template, url_for, flash, abort, redirect, session, request
from flask_login import login_required,current_user
from app.models.tables import Funcionario, Agencia, User
from app.models.decorators import verifica_autorizacao, verifica_autorizacao_or_is_user, verifica_autorizacao_num
from app.models.forms import CreateFuncionarioForm, EditFuncionarioForm
from app import conn,app
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError

@app.route('/funcionario/create',methods=["GET","POST"],endpoint='createFuncionario')
@login_required
@verifica_autorizacao(2)
def createFuncionario():
    if not current_user.username in session:
        flash("Cadastre o acesso para o funcionário antes de prosseguir!")
        return redirect(url_for('register',path='funcionario'))
    else:
        sessao = session[current_user.username]
    form = CreateFuncionarioForm()
    access = ["Cliente","Funcionário","Gerente","Administrador"]

    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")

##############   Pegando agências para o form ###########
    cursor.execute("SELECT * FROM agencia")
    di = cursor.fetchall()
    agencia = []
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        agencia += [Agencia(d).getChoice()]
    form.agencia.choices = agencia
#############################################################

###########  Pegando Supervisores para o form ################
    print(di)
    cursor.execute("SELECT * FROM funcionario INNER JOIN users ON num_func = id")
    di = cursor.fetchall()
    supervisores = []
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        supervisores += [Funcionario(d).getChoice()]
    form.supervisor.choices = supervisores
###########################################################

    if form.validate_on_submit():
        try:
            user = User(sessao)
            user.generate_password()
            cursor.execute("INSERT INTO users(username,password,level,is_func,nome,telefone) VALUES('%s','%s','%s','TRUE','%s','%s')" % (user.username,user.password,user.level,form.name.data,form.phone.data))
            cursor.execute("SELECT id FROM users WHERE username = '%s'"%(user.username))
            di = cursor.fetchone()
            cursor.execute("INSERT INTO funcionario(num_func,nome_ag,supervisor) VALUES('%s','%s','%s')" % (di[0],form.agencia.data,form.supervisor.data))
            conn.commit()
            session.pop(current_user.username,None)
            flash("Funcionário Criado!")
            return redirect(url_for('getFuncionario',agencia=form.agencia.data))
        except IntegrityError as error:
            if error.pgcode == '23505':
                flash('Usuário já utilizado')
            conn.rollback()
            return redirect(url_for('register',path='funcionario'))
        except Exception as error:
            conn.rollback()
            print(error,end="\n\n\n")
            flash('Desculpe, tivemos um problema. Tente novamente!')
            return redirect(url_for('register',path='funcionario'))
    return render_template('createFuncionario.html', access=access[int(sessao['level'])],form=form,sessao=sessao)


@app.route("/funcionario/get", endpoint='getFuncionario')
@login_required
@verifica_autorizacao(1)
def getFuncionario():
    agencia = request.args.get('agencia')
    if not agencia:
        return redirect(url_for('getAgencia',opcao='funcionario'))
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    cursor.execute("SELECT * FROM funcionario INNER JOIN users ON num_func = id WHERE nome_ag = '%s'" %(agencia))
    di = cursor.fetchall()
    funcionarios = []
    access = ["Cliente","Funcionário","Gerente","Administrador"]
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        funcionarios += [Funcionario(d)]
    return render_template('getFuncionarios.html',funcionarios=funcionarios,access=access)

@app.route('/funcionario/edit/<int:num_func>',methods=["GET","POST"], endpoint='editFuncionario')
@login_required
@verifica_autorizacao_or_is_user(2)
def editFuncionario(num_func):
    form = EditFuncionarioForm()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    access = ["Cliente","Funcionário","Gerente","Administrador"]

    ###########  Pegando Agencia para o form ################
    cursor.execute("SELECT * FROM agencia")
    di = cursor.fetchall()
    agencia = []
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        agencia += [Agencia(d).getChoice()]
    form.nome_ag.choices = agencia
    ###########################################################

    ###########  Pegando Supervisores para o form ################
    cursor.execute("SELECT * FROM funcionario INNER JOIN users ON num_func = id")
    di = cursor.fetchall()
    supervisores = []
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        supervisores += [Funcionario(d).getChoice()]
    form.supervisor.choices = supervisores
    ###########################################################
    cursor.execute("""SELECT * FROM users
                    INNER JOIN funcionario ON id = num_func
                    WHERE num_func = '%s'""" %(num_func))
    di = cursor.fetchone()
    user = {}
    for key,value in di._index.items():
        user[key] = di[value]
    user = User(user)
    if form.validate_on_submit():
        if not current_user.check_password(form.youpassword.data):
            flash("Sua senha é Inválida!")
            return redirect(url_for('editFuncionario',num_func=num_func))

        try:
            func = ["nome_ag"]
            us = ["level","password","telefone","nome"]
            insert = ""
            for key,value in form.data.items():
                if key in func and (type(value) is str and len(value) > 1 or type(value) != str):
                    insert += "%s = '%s',"%(key,value)

            cursor.execute("""UPDATE funcionario
                            SET %s
                            WHERE num_func = %r""" %(insert[0:len(insert)-1],num_func))

            u = User({'password':form.password.data,'level':form.level.data})
            if form.password.data is "":
                u.password = user.password
            else:
                u.generate_password()

            cursor.execute("""UPDATE users
                            SET password = '%s', level = '%s'
                            WHERE id = '%s'""" %(u.password,u.level,user.id))
            conn.commit()
            flash("Usuário atualizado")
            return redirect(url_for('editFuncionario',num_func=num_func))
        except Exception as error:
            print(error)
            conn.rollback()
    form.level.data = str(user.level)
    return render_template('funcionario.html',form=form,user=user)

@app.route('/funcionario/delete/<int:num_func>', endpoint='deleteFuncionario')
@login_required
@verifica_autorizacao_num(2)
def deleteFuncionario(num_func):
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    try:
        cursor.execute("DELETE FROM funcionario WHERE num_func= %s"%(num_func))
        cursor.execute("DELETE FROM users WHERE id= %s"%(num_func))
        conn.commit()
        flash("O Funcionario foi excluido")
        return redirect(url_for('getFuncionario'))
    except Exception as error:
        flash("Tivemos um problema, tente novamente!")
        return redirect(url_for('getFuncionario'))


