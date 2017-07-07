from app import conn,app
from app.models.tables import User, Cliente, Funcionario, Agencia, Conta, Operacao
from app.models.forms import CreateContaForm1, CreateContaForm, GetContaForm, \
                             CreateOperacaoForm,CreateEmprestimoForm
from flask import request,flash,render_template,url_for,redirect
from flask_login import login_required, current_user
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError



@app.route('/conta/get', methods=["GET","POST"],endpoint='getConta')
@login_required
def getConta():
    opcao = request.args.get('opcao')
    if opcao == "create":
        form = CreateContaForm1()
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("SET search_path TO agencia")
        ###########  Pegando Agencias para o form ################
        cursor.execute("SELECT * FROM agencia")
        di = cursor.fetchall()
        agencias = []
        for i in range(0,len(di)):
            d = {}
            for key,value in di[i]._index.items():
                d[key] = di[i][value]
            agencias += [Agencia(d).getChoice()]
        form.agencia.choices = agencias
        ###########################################################
        if request.method == "POST" and form.validate_on_submit:
            if form.tipo.data == "1" or form.tipo.data == "2":
                return redirect(url_for("createConta",agencia=form.agencia.data,tipo=form.tipo.data))
            else:
                flash("Tivemos um problema tente novamente!")
                return redirect(url_for('dashboard'))
                #return redirect(url_for('getConta',opcao='create'))
        return render_template('createConta1.html', form=form)
    elif opcao == "get":
        op = request.args.get('op')
        form = GetContaForm()
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("SET search_path TO agencia")
        cursor.execute("""SELECT * FROM conta
                        INNER JOIN mantem_conta
                        ON conta.numero = mantem_conta.numero AND conta.agencia = mantem_conta.agencia
                        WHERE mantem_conta.cliente = '%s'""" %(current_user.id))
        di = cursor.fetchall()
        contas = []
        for i in range(0,len(di)):
            d = {}
            for key,value in di[i]._index.items():
                d[key] = di[i][value]
            contas += [Conta(d).getChoice()]
        form.conta.choices = contas
        if form.validate_on_submit():
            if op == "saldo":
                return redirect(url_for('saldoConta',conta=form.conta.data))
            elif op == "extrato":
                return redirect(url_for('extratoConta',conta=form.conta.data))
            elif op == "pagamento":
                return redirect(url_for('pagamentoConta',conta=form.conta.data))
            else:
                flash("Tivemos um problema, Tente novamente")
                return redirect(url_for('dashboard'))
        return render_template('getConta.html', form=form)
    else:
        flash("Opção inválida acesse usando o menu a direita :(")
        return redirect(url_for('dashboard'))

@app.route('/conta/create', methods=["GET","POST"], endpoint='createConta')
@login_required
def createConta():
    ag = request.args.get('agencia')
    tipo = request.args.get('tipo')
    if not ag or not tipo:
        flash('Tivemos um problema tente novamente :(')
        return redirect(url_for('getConta',opcao="create"))

    form = CreateContaForm()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")

    #################          Pegando Agencia a conta          ################
    cursor.execute("SELECT * from agencia WHERE nome = '%s'" %(ag))
    di = cursor.fetchone()
    agencia = []
    d = {}
    for key,value in di._index.items():
        d[key] = di[value]
    agencia = Agencia(d)
    ############################################################################

    ###########  Pegando Clientes para o form ################
    cursor.execute("SELECT * FROM cliente INNER JOIN users ON cliente.id = users.id")
    di = cursor.fetchall()
    clientes = []
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        clientes += [Cliente(d).getChoice()]
    form.users.choices = clientes
    ###########################################################
    if request.method == "POST" and form.validate_on_submit:
        if tipo == "1":
            try:
                tarifa = float(form.tarifa.data)
                inicial = float(form.valorInicial.data)
                cursor.execute("INSERT INTO conta(agencia,tarifa,saldo,is_corrente) VALUES('%s','%s','%s','TRUE')"%(agencia.nome,tarifa,inicial))
                cursor.execute("SELECT MAX(numero) FROM CONTA")
                di = cursor.fetchone()
                for u in form.users.data:
                    cursor.execute("INSERT INTO mantem_conta(cliente,numero,agencia) VALUES('%s','%s','%s')"%(u,di[0],agencia.nome))
                conn.commit()
            except ValueError as error:
                flash("Por favor insira valores com ponto flutuante ex.: 12.0")
                return redirect(url_for("createConta",agencia=ag,tipo=tipo))
            except Exception as error:
                print(error)
                conn.rollback()
                flash("Desculpe tivemos um problema, tente novamente :(")
                return redirect(url_for("createConta",agencia=ag,tipo=tipo))
        elif tipo == "2":
            try:
                taxa = float(form.taxa.data)
                inicial = float(form.valorInicial.data)
                cursor.execute("INSERT INTO conta(agencia,taxa,saldo,is_corrente) VALUES('%s','%s','%s','FALSE')"%(agencia.nome,taxa,inicial))
                cursor.execute("SELECT MAX(numero) FROM CONTA")
                di = cursor.fetchone()
                for u in form.users.data:
                    cursor.execute("INSERT INTO mantem_conta(cliente,numero,agencia) VALUES('%s','%s','%s')"%(u,di[0],agencia.nome))
                conn.commit()
            except ValueError as error:
                print("erro de conversão")
                flash("Por favor insira valores com ponto flutuante ex.: 12.0")
                return redirect(url_for("createConta",agencia=ag,tipo=tipo))
            except Exception as error:
                print(error)
                conn.rollback()
                flash("Desculpe tivemos um problema, tente novamente :(")
                return redirect(url_for("createConta",agencia=ag,tipo=tipo))
        flash("Conta Criada com Sucesso!")
        return redirect(url_for('getConta',opcao="create"))
    return render_template('createConta.html',form=form,tipo=tipo,agencia=agencia)


@app.route('/conta/saldo', endpoint='saldoConta')
@login_required
def saldoConta():
    conta = request.args.get('conta')
    conta = conta.split(';')
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    cursor.execute("SELECT * FROM conta WHERE numero = '%s' AND agencia = '%s'"%(conta[0],conta[1]))
    di = cursor.fetchone()
    contas = []
    d = {}
    for key,value in di._index.items():
        d[key] = di[value]
    contas = Conta(d)

    return render_template('saldo.html',conta=contas)


@app.route('/conta/extrato', endpoint='extratoConta')
@login_required
def extratoConta():
    conta = request.args.get('conta')
    conta = conta.split(';')
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    cursor.execute("SELECT * FROM operacao_bancaria WHERE numero_co = '%s' AND agencia = '%s' ORDER BY data_op"%(conta[0],conta[1]))
    di = cursor.fetchall()
    operacoes = []
    d = {}
    for i in range(0,len(di)):
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        operacoes += [Operacao(d)]
    return render_template('extrato.html',operacoes=operacoes)

@app.route('/conta/pagamento', methods=["GET","POST"], endpoint='pagamentoConta')
@login_required
def pagamentoConta():
    my = request.args.get('conta')
    if not my:
        flash('Escolha uma conta!')
        return redirect(url_for('getConta',opcao="get",op='pagamento'))
    my = my.split(';')
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SET search_path TO agencia")
    form = CreateOperacaoForm()
    ###########  Pegando Contas para o form ################
    cursor.execute("SELECT * FROM conta")
    di = cursor.fetchall()
    contas = []
    for i in range(0,len(di)):
        d = {}
        for key,value in di[i]._index.items():
            d[key] = di[i][value]
        contas += [Conta(d).getChoice()]
    form.conta.choices = contas
    ###########################################################
    if request.method == "POST" and form.validate_on_submit:
        try:
            if current_user.check_password(form.senha.data):
                valor = float(form.valor.data)
                print(form.conta.data)
                numero,agencia = form.conta.data.split(';')
                cursor.execute("""INSERT INTO operacao_bancaria(numero_co,agencia,descricao,valor,tipo)
                                VALUES ('%s','%s','%s','%s','debito'),
                                ('%s','%s','%s','%s','credito')
                                """%(my[0],my[1],form.descricao.data,valor, \
                                numero,agencia,form.descricao.data,valor))
                if cursor.rowcount < 2:
                    conn.rollback()
                    flash("Saldo Insuficiente")
                    return redirect(url_for('pagamentoConta',conta = (my[0]+";"+my[1])))
                else:
                    conn.commit()
                    flash('Pagamento Realizado!')
            else:
                flash('Senha Inválida!')
                return redirect(url_for('pagamentoConta',conta = (my[0]+";"+my[1])))
            return redirect(url_for('dashboard'))
        except ValueError as error:
            print(error)
            print(form.valor.data)
            flash("Insira um valor valido!")
            return redirect(url_for('pagamentoConta',conta=(my[0]+";"+my[1])))
        except Exception as error:
            print(error)
            conn.rollback()
            flash("ERROR!")
            return redirect(url_for('dashboard'))


    return render_template('pagamento.html',form=form)


@app.route('/conta/emprestimo', methods=["GET","POST"], endpoint='emprestimoConta')
@login_required
def emprestimoConta():
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("SET search_path TO agencia")
        form = CreateEmprestimoForm()

        ###########  Pegando Agencia para o form ################
        cursor.execute("SELECT * FROM agencia")
        di = cursor.fetchall()
        agencias = []
        for i in range(0,len(di)):
            d = {}
            for key,value in di[i]._index.items():
                d[key] = di[i][value]
            agencias += [Agencia(d).getChoice()]
        form.agencia.choices = agencias
        ###########################################################

        ###########  Pegando Contas para o form ################
        cursor.execute("""SELECT * FROM conta AS c
                        INNER JOIN mantem_conta AS mc
                            ON c.numero = mc.numero AND c.agencia = mc.agencia
                            WHERE cliente = '%s'"""%(current_user.id))
        di = cursor.fetchall()
        contas = []
        for i in range(0,len(di)):
            d = {}
            for key,value in di[i]._index.items():
                d[key] = di[i][value]
            contas += [Conta(d).getChoice()]
        form.conta.choices = contas
        ###########################################################

        ###########  Pegando Pessoas para o form ################
        cursor.execute("SELECT * FROM cliente INNER JOIN users ON users.id = cliente.id")
        di = cursor.fetchall()
        pessoas = []
        for i in range(0,len(di)):
            d = {}
            for key,value in di[i]._index.items():
                d[key] = di[i][value]
            pessoas += [Cliente(d).getChoice()]
        form.pessoas.choices = pessoas
        ###########################################################
        if request.method == "POST" and form.validate_on_submit:
            try:
                if current_user.check_password(form.senha.data):
                    valor = float(form.valor.data)
                    agencia = form.agencia.data
                    cursor.execute("""INSERT INTO emprestimo(valor,agencia,qtd_parcelas)
                                    VALUES ('%s','%s','%s')
                                    """%(valor,form.agencia.data, \
                                    form.parcelas.data))
                    #conn.commit()
                    cursor.execute("SELECT MAX(id) FROM emprestimo")
                    di = cursor.fetchone()
                    di = di[0]
                    for u in form.pessoas.data:
                        cursor.execute("""INSERT INTO mantem_emprestimo(id_cliente,id_emprestimo)
                                        VALUES('%s','%s')"""%(u,di))
                    #conn.commit()
                    my = form.conta.data.split(";")
                    cursor.execute("""INSERT INTO operacao_bancaria(numero_co,agencia,descricao,valor,tipo)
                                    VALUES ('%s','%s','Empréstimo','%s','credito')
                                    """%(my[0],my[1],valor))
                    conn.commit()
                    flash('Emprestimo Realizado!')
                else:
                    flash('Senha Inválida!')
                    return redirect(url_for('emprestimoConta'))
                return redirect(url_for('dashboard'))
            except ValueError as error:
                flash("Insira um valor valido!")
                return redirect(url_for('emprestimoConta'))
            except Exception as error:
                print(error)
                conn.rollback()
                flash("ERROR!")
                return redirect(url_for('dashboard'))
        return render_template('emprestimo.html',form=form)