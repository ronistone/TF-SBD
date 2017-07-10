-----------------------------------------------------------------------
-----------                   Atualização                --------------
-----------------------------------------------------------------------

-- -----------------------------------------------------
-- Inserção
-- -----------------------------------------------------
INSERT INTO agencia VALUES('Acaraú','Uberlândia','MG');


-- -----------------------------------------------------
-- Remoção
-- -----------------------------------------------------

-- Remove o usuário seja ele cliente ou funcionario
-- (e caso seja funcionario todas as linhas da tabela
-- dependente que são dependentes)
-- desde que ele não conta, cupom e emprestimo
DELETE FROM users WHERE 1;

-- Remove uma operacao bancaria desde que não tenha
-- um cupom
DELETE FROM operacao_bancaria WHERE 3;

-- Remove todos os cupons do banco
DELETE FROM cupom;

-- -----------------------------------------------------
-- Atualização
-- -----------------------------------------------------

-- Atualiza o nome da uma agência
UPDATE agencia SET nome = 'BATATA' WHERE nome = 'Acaé';

-- Atualiza o saldo de todas as contas
UPDATE conta SET saldo = 100000;

-- Atualiza a validade do cupom para a data de nascimento
-- do cliente de id 6
UPDATE cupom SET validade = a.data_nasc
  FROM (SELECT data_nasc FROM cliente WHERE id = 6) a;