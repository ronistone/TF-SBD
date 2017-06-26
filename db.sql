DROP SCHEMA IF EXISTS agencia CASCADE;
CREATE SCHEMA agencia;
SET search_path TO agencia;
CREATE TABLE agencia(
  nome    VARCHAR(50) ON UPDATE CASCADE ON DELETE NO ACTION,
  cidade  VARCHAR(50),
  estado  VARCHAR(3),
  CONSTRAINT pk_agencia PRIMARY KEY(nome)
);
CREATE TABLE users(
  id SERIAL,
  username  VARCHAR(30) UNIQUE NOT NULL,
  password  VARCHAR(500)  NOT NULL,
  level     INTEGER DEFAULT 0,
  is_func   BOOLEAN DEFAULT 'FALSE',
  CONSTRAINT pk_user  PRIMARY KEY(id),
  CONSTRAINT ck_level CHECK(level >= 0 AND level <= 3)
);
CREATE TABLE funcionario(
  num_func      SERIAL,
  nome          VARCHAR(50) NOT NULL,
  telefone      CHAR(12) NOT NULL,
  data_admissao DATE DEFAULT NOW(),
  id_user       INTEGER NOT NULL,
  nome_ag       VARCHAR(50),
  CONSTRAINT fk_agencia FOREIGN KEY(nome_ag) REFERENCES agencia,
  CONSTRAINT fk_user    FOREIGN KEY(id_user) REFERENCES users,
  CONSTRAINT pk_func    PRIMARY KEY(num_func)
);
CREATE TABLE cliente(
  id        SERIAL,
  nome      VARCHAR(30) NOT NULL,
  cpf       VARCHAR(12) NOT NULL,
  data_nasc DATE,
  endereco  VARCHAR(60),
  cidade    VARCHAR(60),
  estado    VARCHAR(3),
  telefone  VARCHAR(12),
  id_user     INTEGER NOT NULL,
  CONSTRAINT fk_user FOREIGN KEY (id_user) REFERENCES users,
  CONSTRAINT pk_cliente PRIMARY KEY(id)
);
INSERT INTO users(username,password,level,is_func)  VALUES('roni','1234',3,'TRUE');
INSERT INTO users(username,password)                VALUES('ronistone','1234');
INSERT INTO agencia(nome,cidade,estado)             VALUES('Banco Do Brasil','Araguari','MG');
INSERT INTO funcionario(nome,telefone,id_user,nome_ag)      VALUES ('Ronistone Junior','034991280104',1,'Banco Do Brasil');
INSERT INTO cliente(nome,cpf,data_nasc,endereco,cidade,estado,telefone,id_user) VALUES('Ronistone','11525491628','05-09-1997','Rua Coronel Povoa, 795','Araguari','MG','034991280104',2);