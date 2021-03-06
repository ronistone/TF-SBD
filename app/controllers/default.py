from flask import render_template,redirect,url_for,flash,request,session
from flask_login import login_user,logout_user, login_required, current_user
from app import app,lm,conn
from app.models.tables import User, Operacao, Cliente
from app.models.forms import LoginForm, RegisterForm
from app.models.decorators import verifica_autorizacao
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError
import json
#cursor = conn.cursor(cursor_factory=DictCursor)

@lm.user_loader
def user_loader(id):
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia;")
    if id[1]:
        cursor.execute("SELECT * FROM users INNER JOIN funcionario ON num_func = users.id WHERE users.id = " + str(id[0])+";")
    else:
        cursor.execute("SELECT * FROM users INNER JOIN cliente ON cliente.id = users.id WHERE users.id = " + str(id[0])+";")
    user = cursor.fetchone()
    if user is None:
        return None
    user = User(user)
    if user:
        return user
    else:
        return None


@app.route('/', endpoint='index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    try:
        if not current_user.is_func:
            operacoes = []
            cupons = []
            cursor.execute("""SELECT o.*
                            FROM operacao_bancaria AS o
                                INNER JOIN mantem_conta AS m
                                    ON numero_co = numero AND o.agencia = m.agencia
                                        WHERE cliente = '%s' ORDER BY data_op DESC LIMIT 10"""%(current_user.id))
            di = cursor.fetchall()
            for i in range(0,len(di)):
                d = {}
                for key,value in di[i]._index.items():
                    d[key] = di[i][value]
                operacoes += [Operacao(d)]
            cursor.execute("""SELECT o.*
                            FROM cupom AS o
                                INNER JOIN mantem_conta AS m
                                    ON numero_co = numero AND o.agencia = m.agencia
                                        WHERE cliente = '%s' AND validade >= NOW() ORDER BY validade DESC"""%(current_user.id))
            di = cursor.fetchall()
            for i in range(0,len(di)):
                d = {}
                for key,value in di[i]._index.items():
                    d[key] = di[i][value]
                cupons += [Operacao(d)]
            return render_template('dashboard.html',o=operacoes,cupom=cupons)
        else:
            clientes = []
            cursor.execute("""SELECT c.*,u.nome
                            FROM cliente AS c INNER JOIN users AS u
                                ON c.id = u.id
                                WHERE id_gerente = '%s'"""%(current_user.num_func))
            di = cursor.fetchall()
            for i in range(0,len(di)):
                d = {}
                for key,value in di[i]._index.items():
                    d[key] = di[i][value]
                clientes += [Cliente(d)]
            return render_template('dashboard.html',clientes=clientes)
    except Exception as error:
        conn.rollback()
        print(error)
        flash('Tivemos um Problema')
        return redirect(url_for('index'))

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if form.validate_on_submit():
        try:
            cursor = conn.cursor(cursor_factory=DictCursor)
            cursor.execute("SET search_path TO agencia;")
            cursor.execute("SELECT * FROM users WHERE username = '"+ form.username.data+"';")
            di = cursor.fetchone()
            d = {}
            if di is None:
                flash("Login Inválido")
            else:
                for key,value in di._index.items():
                    d[key] = di[value]
                user = User(d)
                if user.check_password(form.password.data):
                    login_user(user,remember=form.remember_me.data)
                    return redirect(url_for('dashboard'))
                else:
                    flash("Login Inválido")
        except Exception as error:
            print(error)
    elif form.errors:
        print(form.errors)
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',endpoint="register",methods=["GET","POST"])
@login_required
@verifica_autorizacao(1)
def register():
    path = request.args.get('path')
    if path is None or (path == 'funcionario' and path == 'cliente'):
        flash('Para criar um usuário use o menu a direita!')
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if path == 'cliente':
        form.level.choices = [('0','Cliente')]
    elif current_user.level == 3:
        form.level.choices = [('1','Funcionario'),('2','Gerente'),('3','Administrador')]
    elif current_user.level == 2:
        form.level.choices = [('1','Funcionario'),('2','Gerente')]
    elif current_user.level == 1:
        form.level.choices = [('1','Funcionario')]

    if form.validate_on_submit():
            user = User({'id':122312,'username':form.name.data,'password':form.password.data,'level':form.level.data})
            #user.generate_password()
            cursor = conn.cursor(cursor_factory=DictCursor)
            cursor.execute("SET search_path TO agencia")
            #current_user.create = user
            cursor.execute("SELECT COUNT(id) FROM users WHERE username = '%s'" %(user.username))
            di = cursor.fetchone()
            if di[0] != 0:
                flash('Usuário já utilizado')
                return redirect(url_for('register',path=path))
            session[current_user.username] = user.__dict__
            if path != "cliente":
                return redirect(url_for('createFuncionario'))
            else:
                #cursor.execute("INSERT INTO users(username,password) VALUES(%s,%s)" % user.username,user.password)
                #conn.commit()
                return redirect(url_for('createCliente'))
    return render_template('register.html',form=form)

# /--- ERROR HANDLER ---
#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404

@app.errorhandler(401)
def forbidden(e):
    return redirect(url_for('login')),401
# --- ERROR HANDLER ---/