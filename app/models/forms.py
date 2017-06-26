from flask_wtf import FlaskForm
from wtforms import *#StringField, PasswordField, BooleanField,TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from app.static.data import estados,cidades

class RegisterForm(FlaskForm):
	name = StringField("name", validators=[DataRequired()])
	password = PasswordField("password", validators=[DataRequired()])
	email = StringField("email", validators=[Email()])

class LoginForm(FlaskForm):
	username = StringField('username',validators=[DataRequired()])
	password = PasswordField('password',validators=[DataRequired()])
	remember_me = BooleanField('remember_me')

class CreateAgenciaForm(FlaskForm):
	name = StringField("Nome", validators=[DataRequired()])
	city = SelectField("Cidade",choices=cidades,id="cidade")
	state = SelectField("Estado",choices=estados, id="estado")

class CreateFuncionarioForm(FlaskForm):
	name = StringField("Nome", validators=[DataRequired()])
	#phone = StringField("Nome",widget=widget.Input(input_type="tel"))