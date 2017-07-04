DROP SCHEMA IF EXISTS agencia CASCADE;
CREATE SCHEMA agencia;
SET search_path TO agencia;
CREATE TABLE agencia(
  nome    VARCHAR(50),
  cidade  VARCHAR(50),
  estado  VARCHAR(3),
  CONSTRAINT pk_agencia PRIMARY KEY(nome)
);
CREATE TABLE users(
  id SERIAL,
  username  VARCHAR(30) UNIQUE NOT NULL,
  password  VARCHAR(500)  NOT NULL,
  level     INTEGER DEFAULT 0,
  nome      VARCHAR(50) NOT NULL,
  telefone  CHAR(15) NOT NULL,
  is_func   BOOLEAN DEFAULT 'FALSE',
  CONSTRAINT pk_user  PRIMARY KEY(id),
  CONSTRAINT ck_level CHECK(level >= 0 AND level <= 3)
);
CREATE TABLE funcionario(
  num_func      INTEGER PRIMARY KEY,
  data_admissao DATE DEFAULT NOW(),
  nome_ag       VARCHAR(50),
  supervisor    INTEGER,
  CONSTRAINT fk_agencia FOREIGN KEY(nome_ag) REFERENCES agencia(nome) ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_user    FOREIGN KEY(num_func) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_supervisor FOREIGN KEY(supervisor) REFERENCES funcionario(num_func) ON UPDATE CASCADE ON DELETE SET NULL
);
CREATE TABLE cliente(
  id        INTEGER PRIMARY KEY,
  cpf       VARCHAR(15) NOT NULL,
  data_nasc DATE,
  endereco  VARCHAR(60),
  cidade    VARCHAR(60),
  estado    VARCHAR(3),
  id_gerente INTEGER,
  CONSTRAINT fk_gerente FOREIGN KEY(id_gerente) REFERENCES funcionario(num_func) ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_user    FOREIGN KEY(id)         REFERENCES users(id)       ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE dependente(
id_func   integer NOT NULL,
nome_depe varchar(100) NOT NULL,
CONSTRAINT pk_dependente      PRIMARY KEY (id_func,nome_depe),
CONSTRAINT fk_func_dependente FOREIGN KEY (id_func) REFERENCES funcionario(num_func) MATCH SIMPLE
           ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE conta(
  numero        integer NOT NULL,
  agencia       VARCHAR(50) NOT NULL,
  data_criacao  date NOT NULL,
  saldo         numeric(7,2) NOT NULL,
  ultimo_acesso date NOT NULL,
  CONSTRAINT pk_conta         PRIMARY KEY(numero,agencia),
  CONSTRAINT fk_agencia_conta FOREIGN KEY (agencia) REFERENCES agencia(nome) MATCH SIMPLE
           ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE mantem_conta(
  cliente integer NOT NULL,
  numero  integer NOT NULL,
  agencia VARCHAR(50) NOT NULL,
  CONSTRAINT pk_conta_cliente PRIMARY KEY(cliente,numero,agencia),
  CONSTRAINT fk_conta_c       FOREIGN KEY (cliente)        REFERENCES cliente(id) MATCH SIMPLE
             ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_conta_conta   FOREIGN KEY (numero,agencia) REFERENCES conta(numero,agencia) MATCH SIMPLE
             ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE conta_poupanca(
  numero  integer NOT NULL,
  agencia VARCHAR(45) NOT NULL,
  taxa    numeric(3,2) NOT NULL,
  CONSTRAINT pk_conta_poupanca PRIMARY KEY (numero,agencia),
  CONSTRAINT fk_conta_poupanca FOREIGN KEY (numero,agencia) REFERENCES conta(numero,agencia)MATCH SIMPLE
             ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE conta_corrente(
  numero  integer NOT NULL,
  agencia VARCHAR(50) NOT NULL,
  tarifa  numeric(3,2) NOT NULL,
  CONSTRAINT pk_conta_corrente PRIMARY KEY (numero,agencia),
  CONSTRAINT fk_conta_corrente FOREIGN KEY (numero,agencia) REFERENCES conta(numero,agencia)MATCH SIMPLE
             ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE operacao_bancaria(
  numero_op   integer NOT NULL,
  numero_co   integer NOT NULL,
  agencia     VARCHAR(50) NOT NULL,
  valor       numeric(5,2) NOT NULL,
  descricao   VARCHAR(100) NOT NULL,
  data_op     date NOT NULL,
  tipo        varchar(50) NOT NULL,
  CONSTRAINT pk_operacao_b      PRIMARY KEY (numero_op,numero_co, agencia),
  CONSTRAINT fk_operacao_contac FOREIGN KEY(numero_co,agencia) REFERENCES conta_corrente(numero,agencia)MATCH SIMPLE
             ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE cupom(
  numero_op     integer NOT NULL,
  numero_co     integer NOT NULL,
  agencia       VARCHAR(50) NOT NULL,
  numero_cupom  integer NOT NULL,
  validade      date NOT NULL,
  CONSTRAINT pk_cupom PRIMARY KEY (numero_op,numero_co, agencia,numero_cupom),
  CONSTRAINT fk_cupom FOREIGN KEY(numero_op,numero_co,agencia) REFERENCES operacao_bancaria(numero_op,numero_co, agencia) MATCH SIMPLE
             ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE emprestimo(
  id            INTEGER PRIMARY KEY,
  valor         NUMERIC(5,2) NOT NULL,
  qtd_parcelas  INTEGER NOT NULL,
  agencia       VARCHAR(50),
  CONSTRAINT fk_emprestimo FOREIGN KEY(agencia) REFERENCES agencia(nome) ON DELETE NO ACTION
);
CREATE TABLE mantem_emprestimo(
  id_cliente    INTEGER,
  id_emprestimo INTEGER,
  CONSTRAINT pk_m_emprestimo PRIMARY KEY(id_cliente,id_emprestimo),
  CONSTRAINT fk_cliente      FOREIGN KEY(id_cliente)    REFERENCES cliente(id),
  CONSTRAINT fk_emprestimo   FOREIGN KEY(id_emprestimo) REFERENCES emprestimo(id)
);



-----------------------------------------------------------------------
----------                 POVOAMENTO                        ----------
-----------------------------------------------------------------------

INSERT INTO users(username,password,level,nome,telefone,is_func)  VALUES('roni','1234',3,'Roni','034991280104','TRUE');
INSERT INTO users(username,password,level,nome,telefone,is_func)  VALUES('ronistone','1234',2,'Ronistone','034991280104','TRUE');
INSERT INTO users(username,password,level,nome,telefone,is_func)  VALUES('ronistonejunior','1234',1,'Ronistone Junior','034991280104','TRUE');
INSERT INTO users(username,password,nome,telefone)        VALUES('jose','1234','José da Silva','034991280104');
INSERT INTO agencia(nome,cidade,estado)             VALUES('Banco Do Brasil','Araguari','MG');
INSERT INTO funcionario(num_func,nome_ag)
                                                    VALUES (1,'Banco Do Brasil');
INSERT INTO funcionario(num_func,nome_ag)
                                                    VALUES (2,'Banco Do Brasil');
INSERT INTO funcionario(num_func,nome_ag)
                                                    VALUES (3,'Banco Do Brasil');
INSERT INTO cliente(cpf,data_nasc,endereco,cidade,estado,id,id_gerente)
                                                    VALUES('11525491628','05-09-1997','Rua Coronel Povoa, 795','Araguari','MG',4,2);