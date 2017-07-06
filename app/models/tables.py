from werkzeug.security import generate_password_hash, check_password_hash
import json
class User(object):

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return (self.id,self.is_func)

    def getChoice(self):
        return (str(self.num_func),self.nome) if self.is_func else (str(self.id),self.nome)

    def generate_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def __init__(self,args):
        for key,value in args.items():
            setattr(self, key, value)

    def __repr__(self):
        #return json.dumps(self.__dict__)
        return "User: "+str(self.id)+" -- username: "+self.username

class Agencia(object):
    def getChoice(self):
        return (self.nome,self.nome)

    def __init__(self,args):
        for key,value in args.items():
            setattr(self, key, value)
    def __repr__(self):
        return "Agencia: "+self.nome+" -- cidade: "+self.cidade

class Funcionario(object):
    def getChoice(self):
        return (str(self.num_func),self.nome)

    def __init__(self,args):
        for key,value in args.items():
            setattr(self, key, value)

    def __repr__(self):
        return "Funcionario: "+self.nome+" -- num_funcional: "+self.num_func

class Cliente(object):
    def getChoice(self):
        return (str(self.id),self.nome)

    def __init__(self,args):
        for key,value in args.items():
            setattr(self, key, value)

    def __repr__(self):
        return "Cliente: "+self.nome+" -- id: "+self.id

class Conta(object):
    def getChoice(self):
        return (str(str(self.numero)+";"+self.agencia),str(self.numero)+ " - " +self.agencia)

    def __init__(self,args):
        for key,value in args.items():
            setattr(self, key, value)

    def __repr__(self):
        return "Conta -- numero: "+str(self.numero)+" -- agencia: "+self.agencia

class Operacao(object):
    #def getChoice(self):
    #    return (str(self.numero_op+";"+self.numero_co+";"+self.agencia),self.num + " - " +self.agencia)

    def __init__(self,args):
        for key,value in args.items():
            setattr(self, key, value)

    def __repr__(self):
        return "Operação -- num: "+str(self.numero_op)+" -- conta: "+str(self.numero_co)+" agencia: "+self.agencia