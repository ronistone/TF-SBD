import psycopg2
from psycopg2.extras import DictCursor

class Estudante(object):
    def __init__(self,id=None,nome=None,datanasc=None,fac_est=None,cra=None,tutor=None):
        self.id = id
        self.nome = nome
        self.datanasc = datanasc
        self.fac_est = fac_est
        self.cra = cra
        self.tutor = tutor
    def __repr__(self):
        return "Nome: "+self.nome+ \
                "\nData de Nascimento: "+self.datanasc.strftime("%x")+ \
                "\nFaculdade: "+self.fac_est+ \
                "\nCRA: "+str(self.cra)+ \
                "\nTutor: "+self.tutor \
                if self.tutor else  \
                "Nome: "+self.nome+ \
                "\nData de Nascimento: "+self.datanasc.strftime("%x")+ \
                "\nFaculdade: "+self.fac_est+ \
                "\nCRA: "+str(self.cra)
try:
    conn = psycopg2.connect(host='localhost',dbname='universidade',user='postgres',password='1234',port='5432')
    cursor = conn.cursor(cursor_factory=DictCursor)
    print("Conectou! :D")
    cursor.execute("SET search_path TO universidade;")
    cursor.execute("SELECT * FROM estudante;")
    dic = cursor.fetchone()
    print(dict(dic))
    for r in cursor :
        e = Estudante(*r)
        print(e)
        print()
except Exception as error:
    print("Deu Ruim ",error)
