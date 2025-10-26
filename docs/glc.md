<h1 align="center"> 
    GLC
</h1>

Terminais são representados pelos elementos cuja grafia está em maiúsculo, bem como pelos símbolos que estão entre aspas duplas (").

```
    script → commands |
             empty

    empty → ε

    commands → command |
               command commands

    command → truncate

    truncate → TRUNCATE TABLE ID
```