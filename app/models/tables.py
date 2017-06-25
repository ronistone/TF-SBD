from werkzeug.security import generate_password_hash, check_password_hash

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
        return "User: "+str(self.id)+" -- username: "+self.username
