<h1 align="center"> 
    GLC
</h1>

Terminais são representados pelos elementos cuja grafia está em maiúsculo, bem como pelos símbolos que estão entre aspas duplas (").

```
    script → commands | empty

    empty → ε

    commands → command semicolon |
               command commands

    command → truncate |
              insert

    truncate → TRUNCATE TABLE object

    insert → INSERT INTO object LPAREN parameters RPAREN VALUES LPAREN parameters RPAREN |
             INSERT INTO object VALUES LPAREN parameters RPAREN |
             INSERT INTO object LPAREN parameters RPAREN select |
             INSERT INTO object DEFAULT VALUES

    parameters → expression COMMA parameters | expression

    expression → ID |
                 NUM

    semicolon → SEMICOLON | empty

    object → ID | 
             ID DOT ID | 
             ID DOT ID DOT ID  
```

- Um ojeto em um banco de dados pode ser referenciado através de um "identificador",
"schema.identificador" ou "database.schema.identificador".