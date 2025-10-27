<h1 align="center"> 
    GLC
</h1>

Terminais são representados pelos elementos cuja grafia está em maiúsculo, bem como pelos símbolos que estão entre aspas duplas (").

```
    -- Regras iniciais

    script → commands | empty

    commands → command semicolon |
               command commands

    -- Comandos:

    command → truncate |
              insert |
              select

    -- Truncate

    truncate → TRUNCATE TABLE object

    -- Insert

    insert → INSERT INTO object LPAREN parameters RPAREN VALUES LPAREN parameters RPAREN |
             INSERT INTO object VALUES LPAREN parameters RPAREN |
             INSERT INTO object LPAREN parameters RPAREN select |
             INSERT INTO object DEFAULT VALUES
    
    -- Select

    select → SELECT TIMES FROM object alias where |
             SELECT modifier columns FROM object alias where |
             

    where → WHERE bool |
            empty

    columns → ID DOT ID alias columns' |
              ID alias columns' |
              INT alias columns' |
              FLOAT alias columns' |
              STRING alias columns'

    columns' → COMMA columns |
               empty

    alias → AS ID |
            ID |
            empty

    modifier → DISTINCT |
               TOP INT percent ties |
               ALL |
               empty

    percent → INT |
              empty
    
    ties → WITH TIES |
           empty

    -- Booleana

    bool → bool OR bool' |
           bool'

    bool' → bool' AND bool'' |
            bool''
    
    bool'' → NOT bool'' |
             LPAREN bool RPAREN |
             comparison

    -- Comparações

    comparison → expression operator expression 

    operator → EQUAL |
               NOT_EQUAL |
               LESS_THAN |
               LESS_EQUAL |
               GREATER_THAN |
               GREATER_EQUAL |
               BETWEEN |
               IN |
               LIKE |
               IS NULL |
               IS NOT NULL
    
    -- Aritméticas

    expression → expression PLUS term |
                 expression MINUS term |
                 term

    term → term TIMES factor |
           term DIVIDE factor |
           factor
    
    factor → ID |
             INT |
             FLOAT |
             VARCHAR |
             CHAR |
             LPAREN expression RPAREN

    -- Outros
    
    type → TINYINT |
           SMALLINT |
           INT |
           BIGINT |
           BIT |
           DECIMAL LPAREN INT COMMA INT RPAREN |
           NUMERIC LPAREN INT COMMA INT RPAREN |
           MONEY |
           SMALLMONEY |
           FLOAT |
           REAL |
           DATE |
           TIME |
           DATETIME2 |
           DATETIMEOFFSET |
           DATETIME |
           SMALLDATETIME |
           CHAR LPAREN INT RPAREN |
           VARCHAR LPAREN INT RPAREN |
           NCHAR LPAREN INT RPAREN |
           NVARCHAR LPAREN INT RPAREN |
           BINARY LPAREN INT RPAREN |
           VARBINARY LPAREN INT RPAREN |
           JSON |
           VECTOR

    parameters → expression COMMA parameters | expression

    empty → ε

    semicolon → SEMICOLON | empty

    object → ID | 
             ID DOT ID | 
             ID DOT ID DOT ID  
```

- Um ojeto em um banco de dados pode ser referenciado através de um "identificador",
"schema.identificador" ou "database.schema.identificador".