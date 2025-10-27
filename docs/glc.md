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

    insert → INSERT INTO object "(" parameters ")" VALUES "(" parameters ")" |
             INSERT INTO object VALUES "(" parameters ")" |
             INSERT INTO object "(" parameters ")" select |
             INSERT INTO object DEFAULT VALUES

    parameters → expression "," parameters | expression

    expression → ID |
                 NUM

    semicolon → ";" | empty

    object → ID | 
             ID "." ID | 
             ID "." ID "." ID  
```

- Um ojeto em um banco de dados pode ser referenciado através de um "identificador",
"schema.identificador" ou "database.schema.identificador".