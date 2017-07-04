
-----------------------------------------------
-- Criando o esquema universidade
-----------------------------------------------
DROP SCHEMA IF EXISTS banco CASCADE;
CREATE SCHEMA banco;
SET search_path TO banco;


-- CHECK('AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS',
         --     'RO','RR','SC','SP','SE','TO'),
-- -----------------------------------------------------
-- Tabela BANCO
-- -----------------------------------------------------

CREATE TABLE agencia (
id_agencia integer NOT NULL,
cidade varchar(60) NOT NULL,
estado varchar(2)  NOT NULL,
CONSTRAINT pk_agencia PRIMARY KEY(id_agencia));

CREATE TABLE funcionario(
id_funcionario integer NOT NULL,
nome varchar(100) NOT NULL,
data_adm date NOT NULL,
tempo_servico integer NOT NULL,
telefone varchar(11) NOT NULL,
supervisor integer NOT NULL,
trabalha integer NOT NULL,
CONSTRAINT pk_funcionario PRIMARY KEY (id_funcionario),
CONSTRAINT fk_supervisor FOREIGN KEY (supervisor) REFERENCES funcionario (id_funcionario) MATCH SIMPLE
           ON UPDATE CASCADE ON DELETE NO ACTION,
CONSTRAINT fk_trabalha FOREIGN KEY (trabalha) REFERENCES agencia(id_agencia) MATCH SIMPLE
           ON UPDATE NO ACTION ON DELETE NO ACTION);


CREATE TABLE cliente(
id_cliente integer NOT NULL,
CPF varchar(11) NOT NULL,
nome varchar(100) NOT NULL,
data_nascimento date NOT NULL,
endereco varchar(100) NOT NULL,
cidade varchar(100) NOT NULL,
estado varchar(2) NOT NULL,
gerente integer NOT NULL,
CONSTRAINT pk_cliente PRIMARY KEY (id_cliente),
CONSTRAINT fk_gerente FOREIGN KEY (gerente) REFERENCES funcionario (id_funcionario) MATCH SIMPLE
           ON UPDATE CASCADE ON DELETE NO ACTION);

CREATE TABLE dependente(
id_func integer NOT NULL,
nome_depe varchar(100) NOT NULL,
CONSTRAINT pk_dependente PRIMARY KEY (id_func,nome_depe),
CONSTRAINT fk_func_dependente FOREIGN KEY (id_func)REFERENCES funcionario(id_funcionario) MATCH SIMPLE
           ON UPDATE CASCADE ON DELETE CASCADE);


CREATE TABLE conta(
numero integer NOT NULL,
agencia integer NOT NULL,
data_criacao date NOT NULL,
saldo numeric(7,2) NOT NULL,
ultimo_acesso date NOT NULL,
CONSTRAINT pk_conta PRIMARY KEY(numero,agencia),
CONSTRAINT fk_agencia_conta FOREIGN KEY (agencia) REFERENCES agencia(id_agencia) MATCH SIMPLE
           ON UPDATE NO ACTION ON DELETE NO ACTION
);



CREATE TABLE conta_cliente(
cliente integer NOT NULL,
numero integer NOT NULL,
agencia integer NOT NULL,
CONSTRAINT pk_conta_cliente PRIMARY KEY(cliente,numero,agencia),
CONSTRAINT fk_conta_c FOREIGN KEY (cliente) REFERENCES cliente(id_cliente) MATCH SIMPLE
           ON UPDATE NO ACTION ON DELETE NO ACTION,
CONSTRAINT fk_conta_conta FOREIGN KEY (numero,agencia) REFERENCES conta(numero,agencia) MATCH SIMPLE
           ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE TABLE conta_poupanca(
numero integer NOT NULL,
agencia integer NOT NULL,
taxa numeric(3,2) NOT NULL,
CONSTRAINT pk_conta_poupanca PRIMARY KEY (numero,agencia),
CONSTRAINT fk_conta_poupanca FOREIGN KEY (numero,agencia) REFERENCES conta(numero,agencia)MATCH SIMPLE
           ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE TABLE conta_corrente(
numero integer NOT NULL,
agencia integer NOT NULL,
tarifa numeric(3,2) NOT NULL,
CONSTRAINT pk_conta_corrente PRIMARY KEY (numero,agencia),
CONSTRAINT fk_conta_corrente FOREIGN KEY (numero,agencia) REFERENCES conta(numero,agencia)MATCH SIMPLE
           ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE TABLE operacao_bancaria(
numero_op integer NOT NULL,
numero_co integer NOT NULL,
agencia integer NOT NULL,
valor numeric(5,2) NOT NULL,
descricao VARCHAR(100) NOT NULL,
data_op date NOT NULL,
tipo varchar(50) NOT NULL,
CONSTRAINT pk_operacao_b PRIMARY KEY (numero_op,numero_co, agencia),
CONSTRAINT fk_operacao_contac FOREIGN KEY(numero_co,agencia) REFERENCES conta_corrente(numero,agencia)MATCH SIMPLE
           ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE TABLE cupom(
numero_op integer NOT NULL,
numero_co integer NOT NULL,
agencia integer NOT NULL,
numero_cupom integer NOT NULL,
validade date NOT NULL,
CONSTRAINT pk_cupom PRIMARY KEY (numero_op,numero_co, agencia,numero_cupom),
CONSTRAINT fk_cupom FOREIGN KEY(numero_op,numero_co,agencia) REFERENCES operacao_bancaria(numero_op,numero_co, agencia) MATCH SIMPLE
           ON UPDATE NO ACTION ON DELETE NO ACTION);




