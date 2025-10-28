<h1 align="center"> 
    GLC
</h1>

Terminais são representados pelos elementos cuja grafia está em maiúsculo, bem como pelos símbolos que estão entre aspas duplas (").

```
    -- Regras iniciais

    script → commands | 
             empty

    commands → command semicolon |
               command commands

    -- Comandos:

    command → truncate |
              insert |
              select |
              create |
              delete |
              drop   |
              update

    -- Truncate

    truncate → TRUNCATE TABLE object

    -- Insert

    insert → INSERT INTO object LPAREN parameters RPAREN VALUES LPAREN parameters RPAREN |
             INSERT INTO object VALUES LPAREN parameters RPAREN |
             INSERT INTO object LPAREN parameters RPAREN select |
             INSERT INTO object DEFAULT VALUES
    
    -- Select

    select → SELECT TIMES FROM object alias where group order |
             SELECT modifier columns FROM object alias where group order
             
    where → WHERE bool |
            empty

    columns → ID DOT ID alias columns' |
              expression alias columns'

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

    group → GROUP BY columns having |
            empty

    having → HAVING bool |
             empty
    
    order → ORDER BY order' |
            empty
    
    order' → bool order'' COMMA  order' |
             bool order''

    order'' → ASC |
              DESC |
              empty
    
    -- Create
    
    create → create_table |
             create_database |
             create_view
        
    create_table → CREATE TABLE object LPAREN columns_defs RPAREN table_options_opt

    column_defs → column_def |
                  column_def COMMA column_defs

    column_def → ID type column_nullability_opt column_identity_opt column_default_opt column_constraint_list_opt

    column_nullability_opt → NOT NULL |
                             NULL |
                             empty    
                
    column_identity_opt → IDENTITY LPAREN INT COMMA INT RPAREN |
                          empty

    column_default_opt → DEFAULT literal |
                         empty

    column_constraint_list_opt → column_constraint column_constraint_list_opt |
                                 empty

    column_constraint → PRIMARY KEY |
                        UNIQUE |                          
                        CHECK LPAREN boolean_expression RPAREN |
                        REFERENCES object FK_ref_columns_opt

    fk_ref_columns_opt → LPAREN parameters RPAREN |
                         empty

    table_options_opt → table_constraint_list_opt |
                        empty

    table_constraint → CONSTRAINT ID constraint_def |
                       constraint_def
    
    constraint_def → PRIMARY KEY LPARENT parameters RPAREN |
                     INIQUE LPAREN parameters RPAREN |
                     FOREING KEY LPAREN parameters RPAREN REFERENCES object FK_ref_columns_opt |
                     CHECK LPAREN boolean_expression RPAREN

    --REGRA DO CREATE DATABASE

     create_database → CREATE DATABASE object database_options_opt
     
     database_options_opt → database_collation_opt | empty
     
     database_collation_opt

    --REGRA DO CREATE VIEW

     create_view → CREATE VIEW object AS select_stms

     select_stms → SELECT select_list FROM object where_opt

     select_list → ASTERISK |
                   id_list

     id_list → ID |
               ID COMMA id_list               

    -- DELETE
    
    delete → DELETE FROM object where_opt

    where_opt → WHERE boolean_expression |
                empty 

    -- DROP

     drop → DROP drop_type object

     drop_type → TABLE |
                 DATABASE |
                 PROCEDURE |
                 FUNCTION |
                 TRIGGER |
                 VIEW |
                 INDEX |
                 ROLE
                      

     drop → IF EXISTS drop_type object  

    -- UPDATE

     update → UPDATE object SET set_list where_opt

     set_list → setitem |
                set_item COMMA set_list

     ser_item → ID EQUAL expression                  
    
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
             TIMES |
             call |
             LPAREN expression RPAREN

    -- Chamadas de Funções
   
    call → ID LPAREN parameters RPAREN |
           ID LPAREN  RPAREN

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

    semicolon → SEMICOLON |
                empty

    object → ID | 
             ID DOT ID | 
             ID DOT ID DOT ID  
```

- Um ojeto em um banco de dados pode ser referenciado através de um "identificador",
"schema.identificador" ou "database.schema.identificador".
