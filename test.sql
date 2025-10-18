CREATE TABLE CLIENTE (
    ID INT PRIMARY KEY IDENTITY(1,1),
    NOME VARCHAR(100),
    EMAIL VARCHAR(100),
    SALARIO DECIMAL(10, 2)
);

INSERT INTO CLIENTE (ID, NOME, EMAIL) 
    VALUES 
        ('João Silva', 'joao21silva@gmail.com', 1680.50)
        ('Carlos Gomes', 'carlos_ita@gmail.com', 2000.67);

SELECT * FROM CLIENTE;

-- L4M0D WAS HERE

/*
    zBro too.
*/
