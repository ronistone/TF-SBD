from flask_wtf import FlaskForm
from wtforms import *#StringField, PasswordField, BooleanField,TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

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
	city = StringField("Cidade", validators=[DataRequired()])
	state = StringField("Estado", validators=[DataRequired()])

class CreateFuncionarioForm(FlaskForm):
	name = StringField("Nome", validators=[DataRequired()])
	#phone = StringField("Nome",widget=widget.Input(input_type="tel"))