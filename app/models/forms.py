from flask_wtf import FlaskForm
from wtforms import *#StringField, PasswordField, BooleanField,TextAreaField, SubmitField
from wtforms.validators import *#DataRequired, Email
from app.static.data import estados,cidades

########################		 LOGIN		###########################

class RegisterForm(FlaskForm):
	name = StringField("name", validators=[DataRequired()])
	password = PasswordField("password", validators=[DataRequired()])
	level = SelectField("level",validators=[DataRequired()])

class LoginForm(FlaskForm):
	username = StringField('username',validators=[DataRequired()])
	password = PasswordField('password',validators=[DataRequired()])
	remember_me = BooleanField('remember_me')

######################################################################

########################		 Create 		###########################

class CreateAgenciaForm(FlaskForm):
	name = StringField("Nome", validators=[DataRequired()])
	city = SelectField("Cidade",choices=cidades,id="cidade")
	state = SelectField("Estado",choices=estados, id="estado")

class CreateFuncionarioForm(FlaskForm):
	name = StringField("Nome", validators=[DataRequired()])
	phone = StringField("telefone")
	agencia = SelectField("Agencia",id="agencia")
	supervisor = SelectField("supervisor",id="supervisor")

class CreateClienteForm(FlaskForm):
	nome = StringField("Nome", validators=[DataRequired()])
	telefone = StringField("Telefone")
	gerente = SelectField("Gerente",id="gerente")
	cpf = StringField("CPF",validators=[DataRequired()])
	data_nasc = DateField("Nascimento", validators=[DataRequired()])
	endereco = StringField("Endereco", validators=[DataRequired()])
	city = SelectField("Cidade",choices=cidades,id="cidade")
	state = SelectField("Estado",choices=estados, id="estado")

class CreateContaForm1(FlaskForm):
	agencia = SelectField("Agencia",id="agencia")
	tipo = SelectField("tipoConta",choices=[("1","Corrente"),("2","Poupança")],id="tipoConta")

class CreateContaForm(FlaskForm):
	taxa = StringField('taxa')
	tarifa = StringField('tarifa')
	valorInicial = StringField('inicial')
	users = SelectMultipleField('Usuarios')

class CreateOperacaoForm(FlaskForm):
	conta = SelectField('Conta', validators=[DataRequired()])
	valor = StringField('valor',validators=[DataRequired()])
	descricao = StringField('Descricao',validators=[DataRequired()])
	senha = PasswordField('Sua Senha', validators=[DataRequired()])

class CreateEmprestimoForm(FlaskForm):
	agencia = SelectField('agencia', validators=[DataRequired()])
	conta = SelectField('conta', validators=[DataRequired()])
	valor = StringField('valor',validators=[DataRequired()])
	parcelas = SelectField('parcelas',choices=[("3","3"),("6","6"),
												("12","12"),("24","24"),
												("30","30"),("36","36"),
												("42","42"),("48","48")],validators=[DataRequired()])
	pessoas = SelectMultipleField('pessoas',validators=[DataRequired()])
	senha = PasswordField('Sua Senha', validators=[DataRequired()])
###########################################################################

####################		GET		#######################################

class GetAgenciaForm(FlaskForm):
	agencia = SelectField("Agencia",id="agencia")

class GetContaForm(FlaskForm):
	conta = SelectField("Conta", id="conta")

##########################################################################

########################		 EDIT		###########################

class EditAgenciaForm(FlaskForm):
	nome = StringField("Nome",validators=[DataRequired()])
	cidade = SelectField("Cidade",choices=cidades,validators=[DataRequired()],id='cidade')
	estado = SelectField("Estado",choices=estados,validators=[DataRequired()],id='estado')

class EditFuncionarioForm(FlaskForm):
	telefone = StringField("telefone")
	nome_ag = SelectField("Agencia",id="agencia")
	level = SelectField("acesso", choices=[('0',"Cliente"),('1',"Funcionario"),('2',"Gerente"),('3',"Administrador")],id="acesso")
	password = PasswordField('password')
	youpassword = PasswordField('youpassword',validators=[DataRequired()])
	supervisor = SelectField("supervisor",id="supervisor")

class EditClienteForm(FlaskForm):
	id_gerente = SelectField("Gerente",id="gerente")
	cpf = StringField("CPF",validators=[DataRequired()])
	data_nasc = DateField("Nascimento", validators=[DataRequired()])
	endereco = StringField("Endereco", validators=[DataRequired()])
	cidade = SelectField("Cidade",choices=cidades,id="cidade")
	estado = SelectField("Estado",choices=estados, id="estado")
	telefone = StringField("telefone")
	password = PasswordField('password')
	youpassword = PasswordField('youpassword',validators=[DataRequired()])

##########################################################################