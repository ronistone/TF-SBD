from flask_login import current_user
from flask import abort, request, session

def verifica_autorizacao(level):
    def verify(func):
        def func_wrapper():
            if current_user.level < level:
                abort(403)
            else:
                return func()
        return func_wrapper
    return verify

def verifica_autorizacao_agencia(level):
    def verify(func):
        def func_wrapper():
            if current_user.level < level:
                abort(403)
            else:
                agencia = request.args.get('agencia')
                return func(agencia)
        return func_wrapper
    return verify

def destroy_session_argument(func):
    def wrapper():
        func()
        session.pop(current_user.username,None)
    return wrapper