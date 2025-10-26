<h1 align="center"> 
    Análise Sintática
</h1>

<h3 align="center"> 
    1. Elementos Sintáticos
</h3>

Um script SQL consiste em uma sequência de nenhuma ou várias instruções, responsáveis por realizar operações de consulta, inserção, atualização, exclusão, criação ou modificação de uma estrutura do banco de dados. Cada instrução segue uma sintaxe formal definida pela gramática da linguagem SQL.
A regra inicial de um script SQL é apresentada a seguir:

```
    script → commands 
             | empty
```

Onde o script SQL é composto por algums comandos (uma ou mais instruções) ou o script pode estar vazio.

<h3 align="center"> 
    1.1 Comandos da Linguagem
</h3>

A linguagem SQL aceita diversos tipos de comandos que permitem ao usuário interagir com o banco de dados.De forma geral, esses comandos podem ser classificados em algumas categorias principais - [Divisões da Linguagem](lexico.md).


<h3 align="center"> 
    1.2 Expressões 
</h3>

Em SQL, uma expressão é uma combinação de valores, colunas, operadores e funções que gera um resultado. Ela pode incluir cálculos aritméticos, comparações, funções, constantes ou nomes de colunas. Expressões são usadas em comandos como SELECT, WHERE e ORDER BY para calcular valores ou filtrar dados.

<h3 align="center"> 
    1.2.1 Chamadas de Função e Atribuição
</h3>

Em SQL, chamadas de função permitem executar operações pré-definidas ou definidas pelo usuário, onde executam operações e podem retor valores que podem ser usados em expressões ou consultas. Já a atribuição permite armazenar o resultado de expressões ou funções em colunas ou variáveis, sendo usada em comandos como UPDATE ou em blocos de procedimentos.

<h3 align="center"> 
    2. Exemplos de Código
</h3>

A seguir, alguns exemplos de código na Linguagem SQL:

```sql
CREATE DATABASE BD_LOJA;

USE BD_LOJA;

CREATE TABLE TB_FUNC (
	CD_FUNCIONARIO INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
	NOME VARCHAR(60) NOT NULL,
	CPF VARCHAR(11) NOT NULL,
	DT_NASCIMENTO DATETIME
);

SELECT * FROM TB_FUNC;

INSERT INTO TB_FUNC (NOME, CPF, DT_NASCIMENTO)
	VALUES ('Guilherme', '00000000032', '2001-09-02 16:00:00');

DROP TABLE TB_FUNC;
```

```sql
CREATE OR ALTER TRIGGER TG_SOLICITACAO_INSERT_UPDATE
ON TB_SOLICITACAO_ABERTURA_CONTA
AFTER INSERT, UPDATE
AS
BEGIN
	DECLARE @NOME VARCHAR(100),
		    @CPF VARCHAR(20),
		    @EMAIL VARCHAR(100),
		    @RENDA_MENSAL NUMERIC(10,2),
		    @TELEFONE VARCHAR(20),
		    @STATUS VARCHAR(20),
		    @ID_SOLICITACAO INT
	DECLARE CUR_SOLICITACAO CURSOR FOR
	SELECT NOME, CPF, EMAIL, RENDA_MENSAL, TELEFONE, STATUS, ID_SOLICITACAO
	FROM INSERTED
	OPEN CUR_SOLICITACAO
	FETCH CUR_SOLICITACAO
	INTO @NOME, @CPF, @EMAIL, @RENDA_MENSAL, @TELEFONE, @STATUS, @ID_SOLICITACAO
	WHILE @@FETCH_STATUS = 0
	BEGIN
		IF @STATUS = 'EM CADASTRO'
		BEGIN
			IF @TELEFONE IS NOT NULL AND @RENDA_MENSAL IS NOT NULL
			BEGIN
				UPDATE TB_SOLICITACAO_ABERTURA_CONTA
				SET STATUS = 'EM ANALISE'
				WHERE ID_SOLICITACAO = @ID_SOLICITACAO 
			END
		END
		ELSE
		BEGIN
			IF @STATUS = 'APROVADA' AND @CPF NOT IN (SELECT CPF FROM TB_CLIENTE)
			BEGIN
				INSERT INTO TB_CLIENTE(NOME, CPF, EMAIL, RENDA_MENSAL, TELEFONE)
				VALUES(@NOME, @CPF, @EMAIL, @RENDA_MENSAL, @TELEFONE)
				DECLARE @ID_CLIENTE INT = (SELECT ID_CLIENTE FROM TB_CLIENTE WHERE CPF = @CPF)
				INSERT INTO TB_CONTA(ID_CLIENTE, DT_ABERTURA, SALDO, STATUS)
				VALUES(@ID_CLIENTE, GETDATE(), 0, 'BLOQUEADA')
			END
		END
		FETCH CUR_SOLICITACAO
		INTO @NOME, @CPF, @EMAIL, @RENDA_MENSAL, @TELEFONE, @STATUS, @ID_SOLICITACAO
	END
	CLOSE CUR_SOLICITACAO
	DEALLOCATE CUR_SOLICITACAO	
END
```

