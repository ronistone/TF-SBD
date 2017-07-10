-----------------------------------------------
-- Criando o esquema agencia
-----------------------------------------------

DROP SCHEMA IF EXISTS agencia CASCADE;
CREATE SCHEMA agencia;
SET search_path TO agencia;


-- -----------------------------------------------------
-- Tabela AGENCIA
-- -----------------------------------------------------
CREATE TABLE agencia(
  nome    VARCHAR(50),
  cidade  VARCHAR(50),
  estado  VARCHAR(3),
  CONSTRAINT pk_agencia PRIMARY KEY(nome)
);

-- -----------------------------------------------------
-- Tabela USERS
-- -----------------------------------------------------
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

-- -----------------------------------------------------
-- Tabela FUNCIONARIO
-- -----------------------------------------------------
CREATE TABLE funcionario(
  num_func      INTEGER PRIMARY KEY,
  data_admissao DATE DEFAULT NOW(),
  nome_ag       VARCHAR(50),
  supervisor    INTEGER,
  CONSTRAINT fk_agencia FOREIGN KEY(nome_ag) REFERENCES agencia(nome) ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_user    FOREIGN KEY(num_func) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_supervisor FOREIGN KEY(supervisor) REFERENCES funcionario(num_func) ON UPDATE CASCADE ON DELETE SET NULL
);

-- -----------------------------------------------------
-- Tabela CLIENTE
-- -----------------------------------------------------
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

-- -----------------------------------------------------
-- Tabela DEPENDENTE
-- -----------------------------------------------------
CREATE TABLE dependente(
id_func   integer NOT NULL,
nome_depe varchar(100) NOT NULL,
CONSTRAINT pk_dependente      PRIMARY KEY (id_func,nome_depe),
CONSTRAINT fk_func_dependente FOREIGN KEY (id_func) REFERENCES funcionario(num_func) MATCH SIMPLE
           ON UPDATE CASCADE ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Tabela CONTA
-- -----------------------------------------------------
CREATE TABLE conta(
  numero        SERIAL,
  agencia       VARCHAR(50) NOT NULL,
  data_criacao  DATE DEFAULT NOW(),
  saldo         NUMERIC(10,2) DEFAULT 0.0,
  ultimo_acesso TIMESTAMP DEFAULT NOW(),
  is_corrente   BOOLEAN DEFAULT 'TRUE',
  taxa    numeric(4,2), --- Poupança
  tarifa  numeric(4,2), --- Corrente
  CONSTRAINT pk_conta         PRIMARY KEY(numero,agencia),
  CONSTRAINT fk_agencia_conta FOREIGN KEY (agencia) REFERENCES agencia(nome) MATCH SIMPLE
           ON UPDATE CASCADE ON DELETE NO ACTION
);

-- -----------------------------------------------------
-- Tabela MANTEM_CONTA
-- -----------------------------------------------------
CREATE TABLE mantem_conta(
  cliente integer NOT NULL,
  numero  integer NOT NULL,
  agencia VARCHAR(50) NOT NULL,
  CONSTRAINT pk_conta_cliente PRIMARY KEY(cliente,numero,agencia),
  CONSTRAINT fk_conta_c       FOREIGN KEY (cliente)        REFERENCES cliente(id) MATCH SIMPLE
             ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_conta_conta   FOREIGN KEY (numero,agencia) REFERENCES conta(numero,agencia) MATCH SIMPLE
             ON UPDATE CASCADE ON DELETE NO ACTION
);

-- -----------------------------------------------------
-- Tabela OPERACAO_BANCARIA
-- -----------------------------------------------------
CREATE TABLE operacao_bancaria(
  numero_op   SERIAL NOT NULL,
  numero_co   integer NOT NULL,
  agencia     VARCHAR(50) NOT NULL,
  valor       numeric(13,2) NOT NULL,
  descricao   VARCHAR(100) NOT NULL,
  data_op     TIMESTAMP DEFAULT NOW(),
  tipo        varchar(50) NOT NULL,
  CONSTRAINT pk_operacao_b      PRIMARY KEY (numero_op,numero_co, agencia),
  CONSTRAINT fk_operacao_contac FOREIGN KEY(numero_co,agencia) REFERENCES conta(numero,agencia)MATCH SIMPLE
             ON UPDATE CASCADE ON DELETE NO ACTION
);


-- -----------------------------------------------------
-- Tabela CUPOM
-- -----------------------------------------------------
CREATE TABLE cupom(
  numero_cupom  SERIAL NOT NULL,
  numero_op     integer NOT NULL,
  numero_co     integer NOT NULL,
  agencia       VARCHAR(50) NOT NULL,
  validade      date NOT NULL,
  CONSTRAINT pk_cupom PRIMARY KEY (numero_cupom),
  CONSTRAINT fk_cupom FOREIGN KEY(numero_op,numero_co,agencia) REFERENCES operacao_bancaria(numero_op,numero_co, agencia) MATCH SIMPLE
             ON UPDATE CASCADE ON DELETE NO ACTION
);

-- -----------------------------------------------------
-- Tabela EMPRESTIMO
-- -----------------------------------------------------
CREATE TABLE emprestimo(
  id            SERIAL PRIMARY KEY,
  valor         NUMERIC(13,2) NOT NULL,
  qtd_parcelas  INTEGER NOT NULL,
  agencia       VARCHAR(50),
  CONSTRAINT fk_emprestimo FOREIGN KEY(agencia) REFERENCES agencia(nome) ON UPDATE CASCADE ON DELETE NO ACTION
);

-- -----------------------------------------------------
-- Tabela MANTEM_EMPRESTIMO
-- -----------------------------------------------------
CREATE TABLE mantem_emprestimo(
  id_cliente    INTEGER,
  id_emprestimo INTEGER,
  CONSTRAINT pk_m_emprestimo PRIMARY KEY(id_cliente,id_emprestimo),
  CONSTRAINT fk_cliente      FOREIGN KEY(id_cliente)    REFERENCES cliente(id),
  CONSTRAINT fk_emprestimo   FOREIGN KEY(id_emprestimo) REFERENCES emprestimo(id)
);


-----------------------------------------------------------------------
-----------------------------------------------------------------------
-----------------------------------------------------------------------

-----------------------------------------------------------------------
----------                     TRIGGERS                     -----------
-----------------------------------------------------------------------

-- -----------------------------------------------------
-- Criando o CUPOM
-- -----------------------------------------------------
CREATE FUNCTION check_transacao() RETURNS trigger AS
$$
BEGIN
  IF(NEW.valor > 5000) THEN
    INSERT INTO cupom (numero_op,numero_co,agencia,validade)
      VALUES(NEW.numero_op,NEW.numero_co,NEW.agencia,NOW() + INTERVAL '15 days');
  END IF;
  RETURN NULL;
END;$$ language plpgsql;

CREATE TRIGGER trig_cupom AFTER INSERT ON operacao_bancaria
  FOR EACH ROW  EXECUTE PROCEDURE check_transacao();
----------------------------------

-- -----------------------------------------------------
-- Atualizando o Saldo
-- -----------------------------------------------------
CREATE FUNCTION update_transacao() RETURNS trigger AS
$$
DECLARE temp record;
BEGIN
  IF(NEW.tipo = 'credito') THEN
    UPDATE conta SET saldo = saldo + NEW.valor WHERE numero = NEW.numero_co AND agencia = NEW.agencia;
  ELSIF(NEW.tipo = 'debito') THEN
    FOR temp IN SELECT * FROM conta WHERE numero = NEW.numero_co AND agencia = NEW.agencia
    LOOP
      IF(temp.saldo < NEW.valor) THEN
        RAISE NOTICE 'Saldo Insuficiente!';
        RETURN NULL;
      ELSE
        UPDATE conta SET saldo = saldo - NEW.valor WHERE numero = NEW.numero_co AND agencia = NEW.agencia;
      END IF;
    END LOOP;
  ELSE
    RETURN NULL;
  END IF;
  RETURN NEW;
END;$$ language plpgsql;

CREATE TRIGGER trig_saldo BEFORE INSERT ON operacao_bancaria
  FOR EACH ROW  EXECUTE PROCEDURE update_transacao();
---------------------------------


-----------------------------------------------------------------------
-----------------------------------------------------------------------
-----------------------------------------------------------------------

-----------------------------------------------------------------------
----------                   POVOAMENTO                      ----------
-----------------------------------------------------------------------

-- -----------------------------------------------------
--  Povoamento no Banco
-- -----------------------------------------------------

--Agência

INSERT INTO agencia VALUES('Acaé','Uberlândia','MG');
INSERT INTO agencia VALUES('Sabiá','Rio de Janeiro','RJ');
INSERT INTO agencia VALUES('Cachimbó','Araguari','MG');
INSERT INTO agencia VALUES('Araponga','Natal','RN');
INSERT INTO agencia VALUES('Carcará','Uberlândia','MG');

-- Users
INSERT INTO users(username,password,level,nome,telefone,is_func)  VALUES ('roni','1234',3,'Ronistone','034995231204','TRUE'),
                                                                         ('rafads','1234',2,'Rafael','034991678104','TRUE'),
                                                                         ('fabio','1234',1,'Fabio','034991340504','TRUE'),
                                                                         ('maria','1234',1,'Maria Da Silva','034991350567','TRUE'),
                                                                         ('josue','1234',1,'Josué de Oliveira','034991260774','TRUE');

INSERT INTO users(username,password,nome,telefone)                VALUES ('pedro','1234','Pedro Augusto','034996485424'),
                                                                         ('yuri','1234','Yuri José','034994466624'),
                                                                         ('leonardo','1234','Leonardo Pereira','034995487124'),
                                                                         ('marcos','1234','Marcos Josué','034996488020'),
                                                                         ('victor','1234','Victor Hugo','034996486204');

--Funcionários
INSERT INTO funcionario(num_func,nome_ag) VALUES (1,'Acaé'),
                                                 (2,'Sabiá'),
                                                 (3,'Cachimbó'),
                                                 (4,'Araponga'),
                                                 (5,'Sabiá');

-- Cliente
INSERT INTO cliente(id,cpf,data_nasc,endereco,cidade,estado,id_gerente) VALUES (6,'11122233344','1986-05-13','Rua Floriano Peixoto,57','Uberlândia','MG',2),
                                                                               (7,'22233344455','1999-12-20','Avenida Brasil,79','Uberlândia','MG',2),
                                                                               (8,'33344455566','2000-12-13','Rua Afonso Pena,534','Araguari','MG',5),
                                                                               (9,'44455566677','2003-04-15','Avenida Minas Gerais,1279','Belo Horizonte','MG',4),
                                                                               (10,'55566677788','1994-05-24','Avenida Esperança,1779','Natal','RN',4);

--DEPENDETE

INSERT INTO dependente VALUES (1,'Miguel Oliveira'),
                              (2,'Deusa Maria'),
                              (3,'Pedro Josué'),
                              (2,'Maria Pereira'),
                              (2,'Josefina Silveira');

--Conta
INSERT INTO conta VALUES (DEFAULT,'Acaé',DEFAULT,100.00,DEFAULT,DEFAULT,11.50),
                         (DEFAULT,'Araponga',DEFAULT,50000.00,DEFAULT,DEFAULT,32.00),
                         (DEFAULT,'Acaé',DEFAULT,1254.00,DEFAULT,'FALSE',0.5),
                         (DEFAULT,'Sabiá',DEFAULT,256.00,DEFAULT,'FALSE',0.8),
                         (DEFAULT,'Sabiá',DEFAULT,256.00,DEFAULT,DEFAULT,24.00);

-- Mantem Conta
INSERT INTO mantem_conta VALUES (6,1,'Acaé'),
                                (7,4,'Sabiá'),
                                (8,3,'Acaé'),
                                (6,5,'Sabiá'),
                                (6,2,'Araponga'),
                                (7,2,'Araponga');


-- Operação Bancaria
INSERT INTO operacao_bancaria(numero_co,agencia,valor,descricao,tipo) VALUES (2,'Araponga',10000.0,'Carro','debito'),
                                                                             (1,'Acaé',6000.0,'Carro','credito'),
                                                                             (3,'Acaé',100.0,'Aluguel','debito'),
                                                                             (5,'Sabiá',200.0,'Conta de agua','debito'),
                                                                             (2,'Araponga',30000.0,'Carro','debito');


-- Emprestimo
INSERT INTO emprestimo(valor,qtd_parcelas,agencia)  VALUES (2000,2,'Acaé'),
                                                           (1000,24,'Sabiá'),
                                                           (500,2,'Araponga'),
                                                           (50000,36,'Cachimbó'),
                                                           (10000,36,'Sabiá');

-- Mantem emprestimo
INSERT INTO mantem_emprestimo VALUES (6,1),
                                     (7,2),
                                     (8,3),
                                     (9,4),
                                     (10,5),
                                     (10,1),
                                     (7,4);