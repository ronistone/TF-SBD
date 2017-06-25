from flask import render_template,redirect,url_for,flash
from flask_login import login_user,logout_user, login_required, current_user
from app import app,lm,conn
from app.models.tables import User
from app.models.forms import LoginForm
from psycopg2.extras import DictCursor
import psycopg2

#cursor = conn.cursor(cursor_factory=DictCursor)

@lm.user_loader
def user_loader(id):
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia;")
    if id[1]:
        cursor.execute("SELECT * FROM users INNER JOIN funcionario ON id_user = users.id WHERE users.id = " + str(id[0])+";")
    else:
        cursor.execute("SELECT * FROM users INNER JOIN cliente ON id_user = users.id WHERE users.id = " + str(id[0])+";")
    user = User(cursor.fetchone())
    if user:
        return user
    else:
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

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


# /--- ERROR HANDLER ---
#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404

@app.errorhandler(401)
def forbidden(e):
    return redirect(url_for('login')),401
# --- ERROR HANDLER ---/