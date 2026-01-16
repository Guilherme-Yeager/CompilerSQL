<h1 align="center"> 
    Análise Sintática
</h1>

<h3 align="center"> 
    1. Elementos Sintáticos
</h3>

Um script SQL consiste em uma sequência de nenhuma ou várias instruções, responsáveis por realizar operações de consulta, inserção, atualização, exclusão, criação ou modificação de uma estrutura do banco de dados. Cada instrução segue uma sintaxe formal definida pela gramática da linguagem SQL.
A regra para os comandos de um script SQL é apresentada a seguir:

```
    command → truncate |
              insert |
              select |
              create |
              delete |
              drop   |
              update
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

A seguir, um exemplo de código na linguagem SQL:

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

