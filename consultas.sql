-----------------------------------------------------------------------
-----------                   Consultas                  --------------
-----------------------------------------------------------------------
-- consultas: 10
-- envolvendo 2 ou mais tabelas: 6
-- função de agregação e group by: 5
-- função de agregação e group by e having: 2

-- -----------------------------------------------------
-- Listar o nome dos Clientes que possuem cupom e
-- quantos cupons são.
-- Envolvendo as tabelas users, cliente, mantem_conta e cupom
-- -----------------------------------------------------
SELECT nome, count(numero_cupom) FROM users AS u
  INNER JOIN (cliente AS c
    INNER JOIN (mantem_conta AS mc
      INNER JOIN cupom AS cp
        ON mc.numero = cp.numero_co AND mc.agencia = cp.agencia)
          ON mc.cliente = c.id)
            ON c.id = u.id
              GROUP BY nome;

-- -----------------------------------------------------
-- Listar quais Contas possuem cupons dentro do prazo de validade
-- e quantos são estes cupons
-- Utilizando apenas a tabela cupom
-- -----------------------------------------------------
SELECT numero_co AS "Numero da Conta",
       agencia AS "Agência",
       count(numero_cupom) AS "Quantidade"
          FROM cupom AS cp GROUP BY (numero_co,agencia);

-- -----------------------------------------------------
-- Mostrar quanto de saldo no total cada agência possui
-- Utilizando apenas a tabela conta
-- -----------------------------------------------------

SELECT agencia AS "Agência",
       sum(saldo) AS "Saldo Total"
          FROM conta GROUP BY (agencia);

-- -----------------------------------------------------
-- Listar o nome dos funcionario e quantos clientes ele
-- gerencia
-- Utilizando as tabelas cliente, funcionario e users
-- -----------------------------------------------------

SELECT nome,sum(CASE WHEN c.id IS NULL THEN 0 ELSE 1 END)
  FROM cliente AS c
    RIGHT OUTER JOIN (funcionario AS f
      INNER JOIN users AS u
        ON f.num_func = u.id)
          ON f.num_func = c.id_gerente
            GROUP BY(nome);


-- -----------------------------------------------------
-- Mostrar o nome do cliente que mantem conta e a quantidade de operações
-- bancárias feitas por ela acima de 5000
-- -----------------------------------------------------


SELECT U.nome "Nome",COUNT(CASE WHEN OP.valor > 5000 THEN 1 ELSE 0 END) "Quantidade"
  FROM users U
    LEFT OUTER JOIN (cliente C
      INNER JOIN (mantem_conta M
        INNER JOIN operacao_bancaria OP
          ON OP.numero_co = M.numero AND OP.agencia = M.agencia)
            ON M.cliente = C.id)
              ON C.id = U.id
                  GROUP BY U.nome;

-- -----------------------------------------------------
-- Mostrar o valores existentes de emprestimos com valor acima de 5000
-- -----------------------------------------------------

SELECT valor
  FROM emprestimo
    GROUP BY valor
      HAVING valor > 5000;

-- -----------------------------------------------------
-- Mostrar o nome de quem mantem emprestimos com mais de
-- 12 parcelas
-- -----------------------------------------------------
SELECT distinct(nome)
  FROM users u
    INNER JOIN (cliente c
      INNER JOIN (mantem_emprestimo mc
        INNER JOIN emprestimo e
          ON mc.id_emprestimo = e.id)
            ON mc.id_cliente = c.id)
              ON u.id = c.id
                GROUP BY u.nome,e.qtd_parcelas
                  HAVING e.qtd_parcelas > 12;

-- -----------------------------------------------------
-- Mostra a quantidade de estados que existe agencia e a
-- quantidade de estados onde os clientes moram
-- -----------------------------------------------------
SELECT COUNT(distinct a.estado) "N# estados Agencia",
       COUNT(distinct c.estado) "N# estados Cliente"
  FROM cliente c, agencia a;

-- -----------------------------------------------------
-- Mostrar o nome do funcionario e seus pendentes
-- -----------------------------------------------------
SELECT u.nome, d.nome_depe
  FROM users u
    LEFT OUTER JOIN (funcionario f
      LEFT OUTER JOIN dependente d
        ON d.id_func = f.num_func )
          ON u.id = f.num_func;

-- -----------------------------------------------------
-- Exibir nome dos funcionários que são gerentes
-- -----------------------------------------------------
SELECT nome
  FROM users
    INNER JOIN cliente
      ON cliente.id_gerente = users.id;