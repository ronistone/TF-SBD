from flask_wtf import FlaskForm
from wtforms import *#StringField, PasswordField, BooleanField,TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from app.static.data import estados,cidades

class RegisterForm(FlaskForm):
	name = StringField("name", validators=[DataRequired()])
	password = PasswordField("password", validators=[DataRequired()])
	level = SelectField("level",validators=[DataRequired()])

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
	phone = StringField("telefone")
	agencia = SelectField("Agencia",id="agencia")

class CreateClienteForm(FlaskForm):
	nome = StringField("Nome", validators=[DataRequired()])
	telefone = StringField("Telefone")
	gerente = SelectField("Gerente",id="gerente")
	cpf = StringField("CPF",validators=[DataRequired()])
	data_nasc = DateField("Nascimento", validators=[DataRequired()])
	endereco = StringField("Endereco", validators=[DataRequired()])
	city = SelectField("Cidade",choices=cidades,id="cidade")
	state = SelectField("Estado",choices=estados, id="estado")

class GetAgenciaForm(FlaskForm):
	agencia = SelectField("Agencia",id="agencia")

class EditAgenciaForm(FlaskForm):
	nome = StringField("Nome",validators=[DataRequired()])
	cidade = SelectField("Cidade",choices=cidades,validators=[DataRequired()],id='cidade')
	estado = SelectField("Estado",choices=estados,validators=[DataRequired()],id='estado')

class EditFuncionarioForm(FlaskForm):
	nome = StringField("Nome")
	telefone = StringField("telefone")
	nome_ag = SelectField("Agencia",id="agencia")
	level = SelectField("acesso", choices=[('0',"Cliente"),('1',"Funcionario"),('2',"Gerente"),('3',"Administrador")],id="acesso")
	password = PasswordField('password')
	youpassword = PasswordField('youpassword',validators=[DataRequired()])