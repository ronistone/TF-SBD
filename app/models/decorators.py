from flask_login import current_user
from flask import abort

def verifica_autorizacao(level):
    def verify(func):
        def func_wrapper():
            if current_user.level < level:
                abort(403)
            else:
                return func()
        return func_wrapper
    return verify