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
    def __init__(self,args):
        for key,value in args.items():
            setattr(self, key, value)
    def __repr__(self):
        return "Funcionario: "+self.nome+" -- num_funcional: "+self.num_func
