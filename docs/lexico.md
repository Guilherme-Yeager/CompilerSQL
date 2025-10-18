<h1 align="center"> 
    SQL
</h1>
Versão: Microsoft SQL Server 2025 RC (17.x) - Outubro/2025

<h3 align="center"> 
    1. Sobre o Dialeto
</h3>

O Transact-SQL (T-SQL) é o dialeto proprietário da Microsoft baseado no padrão ANSI SQL, utilizado no SQL Server e no Azure SQL Database. Ele amplia o SQL padrão com extensões procedurais, tratamento de exceções, variáveis locais, transações avançadas, cursors, e integração com IA e APIs externas (novidade da versão 2025).


<h3 align="center"> 
    2. Divisões da Linguagem
</h3>

A linguagem SQL é composta por diferentes subconjuntos, cada um voltado a uma finalidade específica dentro da manipulação e definição de dados. No SQL Server, ela se caracteriza como uma linguagem dentro de um contexto híbrido, pois combina dois paradigmas:

- SQL declarativo — voltado à definição e consulta de dados, descrevendo o que deve ser feito;

- T-SQL imperativo (Transact-SQL) — voltado à lógica procedural, controle de fluxo e tratamento de exceções, descrevendo como as operações devem ser executadas.

As divisões são:

<div align="center">
  <table border="1" cellspacing="0" cellpadding="8">
    <thead>
      <tr>
        <th>Categoria</th>
        <th>Nome Completo</th>
        <th>Função Principal</th>
        <th>Exemplos</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>DDL</strong></td>
        <td><em>Data Definition Language</em></td>
        <td>Define e altera a estrutura do banco de dados (tabelas, índices, schemas etc.).</td>
        <td><code>CREATE</code>, <code>ALTER</code>, <code>DROP</code>, <code>TRUNCATE</code>, <code>RENAME</code></td>
      </tr>
      <tr>
        <td><strong>DML</strong></td>
        <td><em>Data Manipulation Language</em></td>
        <td>Manipula os dados dentro das estruturas criadas.</td>
        <td><code>SELECT</code>, <code>INSERT</code>, <code>UPDATE</code>, <code>DELETE</code>, <code>MERGE</code></td>
      </tr>
      <tr>
        <td><strong>DCL</strong></td>
        <td><em>Data Control Language</em></td>
        <td>Controla permissões e acessos aos dados.</td>
        <td><code>GRANT</code>, <code>REVOKE</code>, <code>DENY</code></td>
      </tr>
      <tr>
        <td><strong>TCL</strong></td>
        <td><em>Transaction Control Language</em></td>
        <td>Gerencia transações e pontos de restauração.</td>
        <td><code>BEGIN TRAN</code>, <code>COMMIT</code>, <code>ROLLBACK</code>, <code>SAVE TRANSACTION</code></td>
      </tr>
      <tr>
        <td><strong>DQL</strong></td>
        <td><em>Data Query Language</em></td>
        <td>Subconjunto de DML, focado exclusivamente em consultas.</td>
        <td><code>SELECT</code>, <code>WHERE</code>, <code>GROUP BY</code>, <code>ORDER BY</code></td>
      </tr>
      <tr>
        <td><strong>Procedural Extensions (T-SQL)</strong></td>
        <td>Extensões proprietárias do SQL Server</td>
        <td>Estruturas de controle, variáveis, cursores e procedimentos.</td>
        <td><code>DECLARE</code>, <code>SET</code>, <code>IF</code>, <code>WHILE</code>, <code>TRY...CATCH</code></td>
      </tr>
    </tbody>
  </table>
</div>


<h3 align="center"> 
    3. Tipo de dados
</h3>

<div align="center">
  <table border="1" cellspacing="0" cellpadding="5">
    <thead>
      <tr>
        <th>Numéricos Exatos</th>
        <th>Numéricos Aproximados</th>
        <th>Data e Hora</th>
        <th>Strings de Caracteres</th>
        <th>Strings Unicode</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>TINYINT</td>
        <td>FLOAT</td>
        <td>DATE</td>
        <td>CHAR</td>
        <td>NCHAR</td>
      </tr>
      <tr>
        <td>SMALLINT</td>
        <td>REAL</td>
        <td>TIME</td>
        <td>VARCHAR</td>
        <td>NVARCHAR</td>
      </tr>
      <tr>
        <td>INT</td>
        <td></td>
        <td>DATETIME2</td>
        <td>TEXT</td>
        <td>NTEXT (obsoleto)</td>
      </tr>
      <tr>
        <td>BIGINT</td>
        <td></td>
        <td>DATETIMEOFFSET</td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td>BIT</td>
        <td></td>
        <td>DATETIME</td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td>DECIMAL(p,s)</td>
        <td></td>
        <td>SMALLDATETIME</td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td>NUMERIC(p,s)</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td>MONEY</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td>SMALLMONEY</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
    </tbody>
  </table>
</div>

<br>

<div align="center">
  <table border="1" cellspacing="0" cellpadding="5">
    <thead>
      <tr>
        <th>Strings Binárias</th>
        <th>Outros Tipos</th>
        <th>Vetores</th>
        <th>JSON</th>
        <th>Tipos Obsoletos</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>BINARY</td>
        <td>SQL_VARIANT</td>
        <td>VECTOR</td>
        <td>JSON</td>
        <td>IMAGE</td>
      </tr>
      <tr>
        <td>VARBINARY</td>
        <td>XML</td>
        <td></td>
        <td></td>
        <td>NTEXT</td>
      </tr>
      <tr>
        <td>IMAGE (obsoleto)</td>
        <td>CURSOR</td>
        <td></td>
        <td></td>
        <td>TEXT</td>
      </tr>
      <tr>
        <td></td>
        <td>ROWVERSION</td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td></td>
        <td>HIERARCHYID</td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td></td>
        <td>UNIQUEIDENTIFIER</td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td></td>
        <td>SQL_VARIANT</td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td></td>
        <td>XML</td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
    </tbody>
  </table>
</div>


<h3 align="center"> 
    4. Palavras Reservadas
</h3>

<div align="center">
  <table border="1" cellspacing="0" cellpadding="5">
    <tbody>
      <tr>
        <td>ADD</td>
        <td>EXTERNAL</td>
        <td>PROCEDURE</td>
        <td>ALL</td>
        <td>FETCH</td>
      </tr>
      <tr>
        <td>PUBLIC</td>
        <td>ALTER</td>
        <td>FILE</td>
        <td>RAISERROR</td>
        <td>AND</td>
      </tr>
      <tr>
        <td>FILLFACTOR</td>
        <td>READ</td>
        <td>ANY</td>
        <td>FOR</td>
        <td>READTEXT</td>
      </tr>
      <tr>
        <td>AS</td>
        <td>FOREIGN</td>
        <td>RECONFIGURE</td>
        <td>ASC</td>
        <td>FREETEXT</td>
      </tr>
      <tr>
        <td>REFERENCES</td>
        <td>AUTHORIZATION</td>
        <td>FREETEXTTABLE</td>
        <td>REPLICATION</td>
        <td>BACKUP</td>
      </tr>
      <tr>
        <td>FROM</td>
        <td>RESTORE</td>
        <td>BEGIN</td>
        <td>FULL</td>
        <td>RESTRICT</td>
      </tr>
      <tr>
        <td>BETWEEN</td>
        <td>FUNCTION</td>
        <td>RETURN</td>
        <td>BREAK</td>
        <td>GOTO</td>
      </tr>
      <tr>
        <td>REVERT</td>
        <td>BROWSE</td>
        <td>GRANT</td>
        <td>REVOKE</td>
        <td>BULK</td>
      </tr>
      <tr>
        <td>GROUP</td>
        <td>RIGHT</td>
        <td>BY</td>
        <td>HAVING</td>
        <td>ROLLBACK</td>
      </tr>
      <tr>
        <td>CASCADE</td>
        <td>HOLDLOCK</td>
        <td>ROWCOUNT</td>
        <td>CASE</td>
        <td>IDENTITY</td>
      </tr>
      <tr>
        <td>ROWGUIDCOL</td>
        <td>CHECK</td>
        <td>IDENTITY_INSERT</td>
        <td>RULE</td>
        <td>CHECKPOINT</td>
      </tr>
      <tr>
        <td>IDENTITYCOL</td>
        <td>SAVE</td>
        <td>CLOSE</td>
        <td>IF</td>
        <td>SCHEMA</td>
      </tr>
      <tr>
        <td>CLUSTERED</td>
        <td>IN</td>
        <td>SECURITYAUDIT</td>
        <td>COALESCE</td>
        <td>INDEX</td>
      </tr>
      <tr>
        <td>SELECT</td>
        <td>COLLATE</td>
        <td>INNER</td>
        <td>SEMANTICKEYPHRASETABLE</td>
        <td>COLUMN</td>
      </tr>
      <tr>
        <td>INSERT</td>
        <td>SEMANTICSIMILARITYDETAILSTABLE</td>
        <td>COMMIT</td>
        <td>INTERSECT</td>
        <td>SEMANTICSIMILARITYTABLE</td>
      </tr>
      <tr>
        <td>COMPUTE</td>
        <td>INTO</td>
        <td>SESSION_USER</td>
        <td>CONSTRAINT</td>
        <td>IS</td>
      </tr>
      <tr>
        <td>SET</td>
        <td>CONTAINS</td>
        <td>JOIN</td>
        <td>SETUSER</td>
        <td>CONTAINSTABLE</td>
      </tr>
      <tr>
        <td>KEY</td>
        <td>SHUTDOWN</td>
        <td>CONTINUE</td>
        <td>KILL</td>
        <td>SOME</td>
      </tr>
      <tr>
        <td>CONVERT</td>
        <td>LEFT</td>
        <td>STATISTICS</td>
        <td>CREATE</td>
        <td>LIKE</td>
      </tr>
      <tr>
        <td>SYSTEM_USER</td>
        <td>CROSS</td>
        <td>LINENO</td>
        <td>TABLE</td>
        <td>CURRENT</td>
      </tr>
      <tr>
        <td>LOAD</td>
        <td>TABLESAMPLE</td>
        <td>CURRENT_DATE</td>
        <td>MERGE</td>
        <td>TEXTSIZE</td>
      </tr>
      <tr>
        <td>CURRENT_TIME</td>
        <td>NATIONAL</td>
        <td>THEN</td>
        <td>CURRENT_TIMESTAMP</td>
        <td>NOCHECK</td>
      </tr>
      <tr>
        <td>TO</td>
        <td>CURRENT_USER</td>
        <td>NONCLUSTERED</td>
        <td>TOP</td>
        <td>CURSOR</td>
      </tr>
      <tr>
        <td>NOT</td>
        <td>TRAN</td>
        <td>DATABASE</td>
        <td>NULL</td>
        <td>TRANSACTION</td>
      </tr>
      <tr>
        <td>DBCC</td>
        <td>NULLIF</td>
        <td>TRIGGER</td>
        <td>DEALLOCATE</td>
        <td>OF</td>
      </tr>
      <tr>
        <td>TRUNCATE</td>
        <td>DECLARE</td>
        <td>OFF</td>
        <td>TRY_CONVERT</td>
        <td>DEFAULT</td>
      </tr>
      <tr>
        <td>OFFSETS</td>
        <td>TSEQUAL</td>
        <td>DELETE</td>
        <td>ON</td>
        <td>UNION</td>
      </tr>
      <tr>
        <td>DENY</td>
        <td>OPEN</td>
        <td>UNIQUE</td>
        <td>DESC</td>
        <td>UNPIVOT</td>
      </tr>
      <tr>
        <td>DISK</td>
        <td>OPENQUERY</td>
        <td>UPDATE</td>
        <td>DISTINCT</td>
        <td>OPENROWSET</td>
      </tr>
      <tr>
        <td>UPDATETEXT</td>
        <td>DISTRIBUTED</td>
        <td>OPENXML</td>
        <td>USE</td>
        <td>DOUBLE</td>
      </tr>
      <tr>
        <td>OPTION</td>
        <td>USER</td>
        <td>DROP</td>
        <td>OR</td>
        <td>VALUES</td>
      </tr>
      <tr>
        <td>DUMP</td>
        <td>ORDER</td>
        <td>VARYING</td>
        <td>ELSE</td>
        <td>OUTER</td>
      </tr>
      <tr>
        <td>VIEW</td>
        <td>END</td>
        <td>OVER</td>
        <td>WAITFOR</td>
        <td>ERRLVL</td>
      </tr>
      <tr>
        <td>PERCENT</td>
        <td>WHEN</td>
        <td>ESCAPE</td>
        <td>PIVOT</td>
        <td>WHERE</td>
      </tr>
      <tr>
        <td>EXCEPT</td>
        <td>PLAN</td>
        <td>WHILE</td>
        <td>EXEC</td>
        <td>PRECISION</td>
      </tr>
      <tr>
        <td>WITH</td>
        <td>EXECUTE</td>
        <td>PRIMARY</td>
        <td>WITHIN GROUP</td>
        <td>EXISTS</td>
      </tr>
      <tr>
        <td>PRINT</td>
        <td>WRITETEXT</td>
        <td>EXIT</td>
        <td>PROC</td>
        <td>EXCEPTION</td>
      </tr>
              <td>ABSOLUTE</td>
        <td>EXEC</td>
        <td>OVERLAPS</td>
        <td>ACTION</td>
        <td>EXECUTE</td>
      </tr>
      <tr>
        <td>ADA</td>
        <td>EXISTS</td>
        <td>PARTIAL</td>
        <td>ADD</td>
        <td>EXTERNAL</td>
      </tr>
      <tr>
        <td>PASCAL</td>
        <td>ALL</td>
        <td>EXTRACT</td>
        <td>POSITION</td>
        <td>ALLOCATE</td>
      </tr>
      <tr>
        <td>FALSE</td>
        <td>PRECISION</td>
        <td>ALTER</td>
        <td>FETCH</td>
        <td>PREPARE</td>
      </tr>
      <tr>
        <td>AND</td>
        <td>FIRST</td>
        <td>PRESERVE</td>
        <td>ANY</td>
        <td>FLOAT</td>
      </tr>
      <tr>
        <td>PRIMARY</td>
        <td>ARE</td>
        <td>FOR</td>
        <td>PRIOR</td>
        <td>AS</td>
      </tr>
      <tr>
        <td>FOREIGN</td>
        <td>PRIVILEGES</td>
        <td>ASC</td>
        <td>FORTRAN</td>
        <td>PROCEDURE</td>
      </tr>
      <tr>
        <td>ASSERTION</td>
        <td>FOUND</td>
        <td>PUBLIC</td>
        <td>AT</td>
        <td>FROM</td>
      </tr>
      <tr>
        <td>READ</td>
        <td>AUTHORIZATION</td>
        <td>FULL</td>
        <td>REAL</td>
        <td>AVG</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>REFERENCES</td>
        <td>BEGIN</td>
        <td>GLOBAL</td>
        <td>RELATIVE</td>
      </tr>
      <tr>
        <td>BETWEEN</td>
        <td>GO</td>
        <td>RESTRICT</td>
        <td>BIT</td>
        <td>GOTO</td>
      </tr>
      <tr>
        <td>REVOKE</td>
        <td>BIT_LENGTH</td>
        <td>GRANT</td>
        <td>RIGHT</td>
        <td>BOTH</td>
      </tr>
      <tr>
        <td>GROUP</td>
        <td>ROLLBACK</td>
        <td>BY</td>
        <td>HAVING</td>
        <td>ROWS</td>
      </tr>
      <tr>
        <td>CASCADE</td>
        <td>HOUR</td>
        <td>SCHEMA</td>
        <td>CASCADED</td>
        <td>IDENTITY</td>
      </tr>
      <tr>
        <td>SCROLL</td>
        <td>CASE</td>
        <td>IMMEDIATE</td>
        <td>SECOND</td>
        <td>CAST</td>
      </tr>
      <tr>
        <td>IN</td>
        <td>SECTION</td>
        <td>CATALOG</td>
        <td>INCLUDE</td>
        <td>SELECT</td>
      </tr>
      <tr>
        <td>CHAR</td>
        <td>INDEX</td>
        <td>SESSION</td>
        <td>CHAR_LENGTH</td>
        <td>SESSION_USER</td>
      </tr>
      <tr>
        <td>CHARACTER</td>
        <td>INITIALLY</td>
        <td>SET</td>
        <td>CHARACTER_LENGTH</td>
        <td>INNER</td>
      </tr>
      <tr>
        <td>SIZE</td>
        <td>CHECK</td>
        <td>INPUT</td>
        <td>SMALLINT</td>
        <td>CLOSE</td>
      </tr>
      <tr>
        <td>INSENSITIVE</td>
        <td>SOME</td>
        <td>COALESCE</td>
        <td>INSERT</td>
        <td>SPACE</td>
      </tr>
      <tr>
        <td>COLLATE</td>
        <td>INT</td>
        <td>SQL</td>
        <td>COLLATION</td>
        <td>INTEGER</td>
      </tr>
      <tr>
        <td>SQLCA</td>
        <td>COLUMN</td>
        <td>INTERSECT</td>
        <td>SQLCODE</td>
        <td>SQLERROR</td>
      </tr>
      <tr>
        <td>CONNECT</td>
        <td>INTO</td>
        <td>SQLSTATE</td>
        <td>CONNECTION</td>
        <td>IS</td>
      </tr>
      <tr>
        <td>SQLWARNING</td>
        <td>CONSTRAINT</td>
        <td>ISOLATION</td>
        <td>SUBSTRING</td>
        <td>CONSTRAINTS</td>
      </tr>
      <tr>
        <td>JOIN</td>
        <td>SUM</td>
        <td>CONTINUE</td>
        <td>KEY</td>
        <td>SYSTEM_USER</td>
      </tr>
      <tr>
        <td>CONVERT</td>
        <td>LANGUAGE</td>
        <td>TABLE</td>
        <td>CORRESPONDING</td>
        <td>LAST</td>
      </tr>
      <tr>
        <td>TEMPORARY</td>
        <td>COUNT</td>
        <td>LEADING</td>
        <td>THEN</td>
        <td>CREATE</td>
      </tr>
      <tr>
        <td>LEFT</td>
        <td>TIME</td>
        <td>CROSS</td>
        <td>LEVEL</td>
        <td>TIMESTAMP</td>
      </tr>
      <tr>
        <td>CURRENT</td>
        <td>LIKE</td>
        <td>TIMEZONE_HOUR</td>
        <td>CURRENT_DATE</td>
        <td>LOCAL</td>
      </tr>
      <tr>
        <td>TIMEZONE_MINUTE</td>
        <td>CURRENT_TIME</td>
        <td>LOWER</td>
        <td>TO</td>
        <td>CURRENT_TIMESTAMP</td>
      </tr>
      <tr>
        <td>MATCH</td>
        <td>TRAILING</td>
        <td>CURRENT_USER</td>
        <td>MAX</td>
        <td>TRANSACTION</td>
      </tr>
      <tr>
        <td>CURSOR</td>
        <td>MIN</td>
        <td>TRANSLATE</td>
        <td>DATE</td>
        <td>MINUTE</td>
      </tr>
      <tr>
        <td>TRANSLATION</td>
        <td>DEALLOCATE</td>
        <td>MONTH</td>
        <td>TRUE</td>
        <td>DEC</td>
      </tr>
      <tr>
        <td>NAMES</td>
        <td>UNION</td>
        <td>DECIMAL</td>
        <td>NATIONAL</td>
        <td>UNIQUE</td>
      </tr>
      <tr>
        <td>DECLARE</td>
        <td>NATURAL</td>
        <td>UNKNOWN</td>
        <td>DEFAULT</td>
        <td>NCHAR</td>
      </tr>
      <tr>
        <td>UPDATE</td>
        <td>DEFERRABLE</td>
        <td>NEXT</td>
        <td>UPPER</td>
        <td>DEFERRED</td>
      </tr>
      <tr>
        <td>NO</td>
        <td>USAGE</td>
        <td>DELETE</td>
        <td>NONE</td>
        <td>USER</td>
      </tr>
      <tr>
        <td>DESC</td>
        <td>NOT</td>
        <td>USING</td>
        <td>DESCRIBE</td>
        <td>NULL</td>
      </tr>
      <tr>
        <td>VALUE</td>
        <td>DESCRIPTOR</td>
        <td>NULLIF</td>
        <td>VALUES</td>
        <td>DIAGNOSTICS</td>
      </tr>
      <tr>
        <td>NUMERIC</td>
        <td>VARCHAR</td>
        <td>DISCONNECT</td>
        <td>OCTET_LENGTH</td>
        <td>VARYING</td>
      </tr>
      <tr>
        <td>DISTINCT</td>
        <td>OF</td>
        <td>VIEW</td>
        <td>DOMAIN</td>
        <td>ON</td>
      </tr>
      <tr>
        <td>WHEN</td>
        <td>DOUBLE</td>
        <td>ONLY</td>
        <td>WHENEVER</td>
        <td>DROP</td>
      </tr>
      <tr>
        <td>OPEN</td>
        <td>WHERE</td>
        <td>ELSE</td>
        <td>OPTION</td>
        <td>WITH</td>
      </tr>
      <tr>
        <td>END</td>
        <td>OR</td>
        <td>WORK</td>
        <td>END-EXEC</td>
        <td>ORDER</td>
      </tr>
      <tr>
        <td>WRITE</td>
        <td>ESCAPE</td>
        <td>OUTER</td>
        <td>YEAR</td>
        <td>EXCEPT</td>
      </tr>
      <tr>
        <td>OUTPUT</td>
        <td>ZONE</td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
    </tbody>
  </table>
</div>


<h3 align="center"> 
    5. Comentários
</h3>

Servem apenas para documentar código. Existem **dois tipos principais de comentários**:

- Comentário de Linha Única - Inicia com dois hífens (`--`) e continua até o final da linha.
- Comentário de Bloco (ou Múltiplas Linhas) - Delimitado por /* no início e */ no final.

**Exemplo:**
```sql
-- Seleciona todos os registros da tabela Clientes
SELECT * FROM Clientes;

SELECT Nome, Idade -- Apenas as colunas Nome e Idade
FROM Pessoas;

/*
    Sou apennas um comentário.
*/
```

<h3 align="center"> 
    6. Operadores
</h3>

No SQL Server, eles podem ser **aritméticos, de comparação, lógicos, de concatenação ou especiais**.

- Operadores Aritméticos
  
  Usados para realizar operações matemáticas em números.

<div align="center">
  <table border="1" cellspacing="0" cellpadding="5">
    <thead>
      <tr>
        <th>Operador</th>
        <th>Descrição</th>
        <th>Exemplo</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>+</td>
        <td>Adição</td>
        <td>5 + 3 → 8</td>
      </tr>
      <tr>
        <td>-</td>
        <td>Subtração</td>
        <td>10 - 4 → 6</td>
      </tr>
      <tr>
        <td>*</td>
        <td>Multiplicação</td>
        <td>6 * 7 → 42</td>
      </tr>
      <tr>
        <td>/</td>
        <td>Divisão</td>
        <td>20 / 4 → 5</td>
      </tr>
      <tr>
        <td>%</td>
        <td>Módulo (resto da divisão)</td>
        <td>10 % 3 → 1</td>
      </tr>
    </tbody>
  </table>
</div>

- Operadores de Comparação

  Usados para comparar valores e retornar **TRUE**, **FALSE** ou **UNKNOWN** (NULL).

<div align="center">
  <table border="1" cellspacing="0" cellpadding="5">
    <thead>
      <tr>
        <th>Operador</th>
        <th>Descrição</th>
        <th>Exemplo</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>=</td>
        <td>Igual a</td>
        <td>ColunaA = 10</td>
      </tr>
      <tr>
        <td>&lt;&gt; ou !=</td>
        <td>Diferente de</td>
        <td>ColunaB &lt;&gt; 5</td>
      </tr>
      <tr>
        <td>&gt;</td>
        <td>Maior que</td>
        <td>Idade &gt; 18</td>
      </tr>
      <tr>
        <td>&gt;=</td>
        <td>Maior ou igual a</td>
        <td>Salario &gt;= 2000</td>
      </tr>
      <tr>
        <td>&lt;</td>
        <td>Menor que</td>
        <td>Quantidade &lt; 100</td>
      </tr>
      <tr>
        <td>&lt;=</td>
        <td>Menor ou igual a</td>
        <td>Nota &lt;= 7</td>
      </tr>
      <tr>
        <td>BETWEEN</td>
        <td>Entre dois valores</td>
        <td>Idade BETWEEN 18 AND 25</td>
      </tr>
      <tr>
        <td>IN</td>
        <td>Pertence a um conjunto</td>
        <td>Estado IN ('SP','RJ')</td>
      </tr>
      <tr>
        <td>LIKE</td>
        <td>Correspondência de padrões</td>
        <td>Nome LIKE 'Jo%'</td>
      </tr>
      <tr>
        <td>IS NULL</td>
        <td>Verifica valores nulos</td>
        <td>DataNascimento IS NULL</td>
      </tr>
      <tr>
        <td>IS NOT NULL</td>
        <td>Verifica valores não nulos</td>
        <td>DataNascimento IS NOT NULL</td>
      </tr>
    </tbody>
  </table>
</div>

- Operadores Lógicos

  Usados para combinar condições em **WHERE**, **HAVING** e expressões booleanas.

<div align="center">
  <table border="1" cellspacing="0" cellpadding="5">
    <thead>
      <tr>
        <th>Operador</th>
        <th>Descrição</th>
        <th>Exemplo</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>AND</td>
        <td>Retorna TRUE se todas forem TRUE</td>
        <td>Idade &gt; 18 AND Ativo = 1</td>
      </tr>
      <tr>
        <td>OR</td>
        <td>Retorna TRUE se pelo menos uma for TRUE</td>
        <td>Estado = 'SP' OR Estado = 'RJ'</td>
      </tr>
      <tr>
        <td>NOT</td>
        <td>Nega a condição</td>
        <td>NOT Ativo = 1</td>
      </tr>
    </tbody>
  </table>
</div>

- Operadores de Concatenação

  Usados para **unir strings**. No SQL Server, o operador principal é o **`+`** para strings:

    ```sql
    SELECT Nome + ' ' + Sobrenome AS NomeCompleto
    FROM Clientes;
    ```

<h3 align="center"> 
    6. Comentários
</h3>

Um **identificador** é o nome dado a **objetos do banco de dados**, como tabelas, colunas, views, índices e procedimentos.

#### Regras principais:
- Pode conter **letras (A-Z, a-z)**, **dígitos (0-9)** e **underscore (_)**.
- O **primeiro caractere** deve ser uma letra ou underscore, a menos que o identificador esteja delimitado por **colchetes []** ou **aspas duplas ""**.
- **Comprimento máximo:** 128 caracteres.
- **Palavras reservadas** não podem ser usadas diretamente; use colchetes ou aspas duplas para contorná-las.
- **Sensibilidade a maiúsculas/minúsculas** depende do `collation` do banco de dados.

#### Exemplos

```sql
-- Válidos
Clientes            -- nome simples
Nome_Produto        -- contém underscore
IDade               -- contém letras e maiúsculas
[Order Details]     -- espaços permitidos com colchetes
"Column-1"          -- caractere especial permitido com aspas duplas

-- Inválidos
123Tabela           -- começa com número
Nome@Produto        -- caractere especial não permitido
SELECT              -- palavra reservada sem colchetes ou aspas
Nome-Produto        -- hífen não permitido sem aspas
Espaço Invalido     -- espaço sem colchetes
````


<h3 align="center"> 
    7. Erros
</h3>

No SQL Server, qualquer sequência de caracteres que **não seja reconhecida como um token válido** (palavra reservada, identificador, literal, operador ou comentário) é considerada um **erro léxico**.  

Durante a análise léxica, o SQL Server **ignora espaços em branco e tabulações** entre tokens. As **quebras de linha** também são ignoradas na execução das instruções, mas **são utilizadas internamente** pelo analisador léxico para rastrear a posição no código, auxiliando na **mensagem de erro** e na indicação da linha onde ocorreu o problema.

Exemplos de erros léxicos:

```sql
SELECT * FROM 123Clientes;    -- Erro: identificador inválido
SELECT @nome# FROM Pessoas;   -- Erro: caractere '#' inválido
SELECT * FROM Produtos WHERE Nome = 'João; -- Erro: literal não fechado
```

<h3 align="center"> 
    7. Referências
</h3>

[1] WILLIAMDASSAFMSFT. Transact-SQL statements. https://learn.microsoft.com/pt-br/sql/t-sql/statements/statements?view=sql-server-ver17.

[2] Microsoft Docs – Reserved Keywords (Transact-SQL)
https://learn.microsoft.com/en-us/sql/t-sql/language-elements/reserved-keywords-transact-sql?view=sql-server-ver17

[3] Microsoft Docs – Data Types (Transact-SQL, PT-BR)
https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17

