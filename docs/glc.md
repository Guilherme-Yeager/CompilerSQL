<h1 align="center"> 
    GLC
</h1>

Terminais são representados pelos elementos cuja grafia está em maiúsculo, bem como pelos símbolos que estão entre aspas duplas (").

```
    -- Regras inicial

    script → empty |
             command SEMICOLON script

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
             INSERT INTO object DEFAULT VALUES
    
    -- Select

    select → SELECT TIMES FROM object |
             SELECT columns FROM object


    columns → columns COMMA object |
              object
    
    -- Create
    
    create → create_table |
             create_database |
        
    create_table → CREATE TABLE object LPAREN columns_defs RPAREN

    column_defs → column_def |
                  column_def COMMA column_defs

    column_def → ID type column_nullability_opt column_identity_opt column_constraint_list_opt

    column_nullability_opt → NOT NULL |
                             NULL |
                             empty    
                
    column_identity_opt → IDENTITY LPAREN INT COMMA INT RPAREN |
                          empty

    column_constraint_list_opt → column_constraint column_constraint_list_opt |
                                 empty

    column_constraint → PRIMARY KEY |
                        UNIQUE

    -- Create Database

     create_database → CREATE DATABASE object
               
    -- Delete
    
    delete → DELETE FROM object |
             DELETE FROM object WHERE expression

    -- Drop

     drop → DROP drop_type object

     drop_type → TABLE |
                 DATABASE

    -- Update

     update → UPDATE object SET set_list expression

     set_list → set_item |
                set_item COMMA set_list

     ser_item → ID EQUAL expression                  

    -- Expressão

    expression → expression_ari |
                 bool
                 
    -- Aritméticas

    expression_ari → expression_ari PLUS term |
                     expression_ari MINUS term |
                     term

    term → term TIMES factor |
           term DIVIDE factor |
           factor

    -- Booleana

    bool → bool OR bool' |
           bool'

    bool' → bool' AND bool'' |
            bool''
    
    bool'' → NOT bool'' |
             LPAREN bool RPAREN |
             comparison

    -- Comparações

    comparison → comparison comp_op comparison' |
                 comparison'

    comparison' → comparison' eq_op comparison'' |
                  comparison''

    comparison'' → factor null_op |
                   factor

    null_op → IS_NULL |
              IS_NOT_NULL
    
    eq_op → EQUAL |
            NOT_EQUAL
    
    comp_op → LESS_THAN |
              LESS_EQUAL |
              GREATER_THAN |
              GREATER_EQUAL
    
    -- Fator

    factor → ID |
             INT |
             STRING |
             LPAREN expression RPAREN

    -- Outros
    
    type → INT |
           STRING
           
    parameters → expression COMMA parameters | expression

    object → ID | 
             ID DOT ID | 
             ID DOT ID DOT ID  
```

- Um ojeto em um banco de dados pode ser referenciado através de um "identificador",
"schema.identificador" ou "database.schema.identificador".
