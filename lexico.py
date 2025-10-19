import ply.lex as lex

reserved = {
    "add": "ADD",
    "external": "EXTERNAL",
    "procedure": "PROCEDURE",
    "all": "ALL",
    "fetch": "FETCH",
    "public": "PUBLIC",
    "alter": "ALTER",
    "file": "FILE",
    "raiserror": "RAISERROR",
    "and": "AND",
    "fillfactor": "FILLFACTOR",
    "read": "READ",
    "any": "ANY",
    "for": "FOR",
    "readtext": "READTEXT",
    "as": "AS",
    "foreign": "FOREIGN",
    "reconfigure": "RECONFIGURE",
    "asc": "ASC",
    "freetext": "FREETEXT",
    "references": "REFERENCES",
    "authorization": "AUTHORIZATION",
    "freetexttable": "FREETEXTTABLE",
    "replication": "REPLICATION",
    "backup": "BACKUP",
    "from": "FROM",
    "restore": "RESTORE",
    "begin": "BEGIN",
    "full": "FULL",
    "restrict": "RESTRICT",
    "between": "BETWEEN",
    "function": "FUNCTION",
    "return": "RETURN",
    "break": "BREAK",
    "goto": "GOTO",
    "revert": "REVERT",
    "browse": "BROWSE",
    "grant": "GRANT",
    "revoke": "REVOKE",
    "bulk": "BULK",
    "group": "GROUP",
    "right": "RIGHT",
    "by": "BY",
    "having": "HAVING",
    "rollback": "ROLLBACK",
    "cascade": "CASCADE",
    "holdlock": "HOLDLOCK",
    "rowcount": "ROWCOUNT",
    "case": "CASE",
    "identity": "IDENTITY",
    "rowguidcol": "ROWGUIDCOL",
    "check": "CHECK",
    "identity_insert": "IDENTITY_INSERT",
    "rule": "RULE",
    "checkpoint": "CHECKPOINT",
    "identitycol": "IDENTITYCOL",
    "save": "SAVE",
    "close": "CLOSE",
    "if": "IF",
    "schema": "SCHEMA",
    "clustered": "CLUSTERED",
    "in": "IN",
    "securityaudit": "SECURITYAUDIT",
    "coalesce": "COALESCE",
    "index": "INDEX",
    "select": "SELECT",
    "collate": "COLLATE",
    "inner": "INNER",
    "semantickeyphrasetable": "SEMANTICKEYPHRASETABLE",
    "column": "COLUMN",
    "insert": "INSERT",
    "semanticsimilaritydetailstable": "SEMANTICSIMILARITYDETAILSTABLE",
    "commit": "COMMIT",
    "intersect": "INTERSECT",
    "semanticsimilaritytable": "SEMANTICSIMILARITYTABLE",
    "compute": "COMPUTE",
    "into": "INTO",
    "session_user": "SESSION_USER",
    "constraint": "CONSTRAINT",
    "is": "IS",
    "set": "SET",
    "contains": "CONTAINS",
    "join": "JOIN",
    "setuser": "SETUSER",
    "containstable": "CONTAINSTABLE",
    "key": "KEY",
    "shutdown": "SHUTDOWN",
    "continue": "CONTINUE",
    "kill": "KILL",
    "some": "SOME",
    "convert": "CONVERT",
    "left": "LEFT",
    "statistics": "STATISTICS",
    "create": "CREATE",
    "like": "LIKE",
    "system_user": "SYSTEM_USER",
    "cross": "CROSS",
    "lineno": "LINENO",
    "table": "TABLE",
    "current": "CURRENT",
    "load": "LOAD",
    "tablesample": "TABLESAMPLE",
    "current_date": "CURRENT_DATE",
    "merge": "MERGE",
    "textsize": "TEXTSIZE",
    "current_time": "CURRENT_TIME",
    "national": "NATIONAL",
    "then": "THEN",
    "current_timestamp": "CURRENT_TIMESTAMP",
    "nocheck": "NOCHECK",
    "to": "TO",
    "current_user": "CURRENT_USER",
    "nonclustered": "NONCLUSTERED",
    "top": "TOP",
    "cursor": "CURSOR",
    "not": "NOT",
    "tran": "TRAN",
    "database": "DATABASE",
    "null": "NULL",
    "transaction": "TRANSACTION",
    "dbcc": "DBCC",
    "nullif": "NULLIF",
    "trigger": "TRIGGER",
    "deallocate": "DEALLOCATE",
    "of": "OF",
    "truncate": "TRUNCATE",
    "declare": "DECLARE",
    "off": "OFF",
    "try_convert": "TRY_CONVERT",
    "default": "DEFAULT",
    "offsets": "OFFSETS",
    "tsequal": "TSEQUAL",
    "delete": "DELETE",
    "on": "ON",
    "union": "UNION",
    "deny": "DENY",
    "open": "OPEN",
    "unique": "UNIQUE",
    "desc": "DESC",
    "unpivot": "UNPIVOT",
    "disk": "DISK",
    "openquery": "OPENQUERY",
    "update": "UPDATE",
    "distinct": "DISTINCT",
    "openrowset": "OPENROWSET",
    "updatetext": "UPDATETEXT",
    "distributed": "DISTRIBUTED",
    "openxml": "OPENXML",
    "use": "USE",
    "double": "DOUBLE",
    "option": "OPTION",
    "user": "USER",
    "drop": "DROP",
    "or": "OR",
    "values": "VALUES",
    "dump": "DUMP",
    "order": "ORDER",
    "varying": "VARYING",
    "else": "ELSE",
    "outer": "OUTER",
    "view": "VIEW",
    "end": "END",
    "over": "OVER",
    "waitfor": "WAITFOR",
    "errlvl": "ERRLVL",
    "percent": "PERCENT",
    "when": "WHEN",
    "escape": "ESCAPE",
    "pivot": "PIVOT",
    "where": "WHERE",
    "except": "EXCEPT",
    "plan": "PLAN",
    "while": "WHILE",
    "exec": "EXEC",
    "precision": "PRECISION",
    "with": "WITH",
    "execute": "EXECUTE",
    "primary": "PRIMARY",
    "exists": "EXISTS",
    "print": "PRINT",
    "writetext": "WRITETEXT",
    "exit": "EXIT",
    "proc": "PROC",
    "exception": "EXCEPTION",
    "absolute": "ABSOLUTE",
    "overlaps": "OVERLAPS",
    "action": "ACTION",
    "ada": "ADA",
    "partial": "PARTIAL",
    "pascal": "PASCAL",
    "extract": "EXTRACT",
    "position": "POSITION",
    "allocate": "ALLOCATE",
    "false": "FALSE",
    "prepare": "PREPARE",
    "first": "FIRST",
    "preserve": "PRESERVE",
    "float": "FLOAT",
    "are": "ARE",
    "prior": "PRIOR",
    "fortran": "FORTRAN",
    "assertion": "ASSERTION",
    "found": "FOUND",
    "at": "AT",
    "real": "REAL",
    "avg": "AVG",
    "get": "GET",
    "global": "GLOBAL",
    "relative": "RELATIVE",
    "bit": "BIT",
    "bit_length": "BIT_LENGTH",
    "both": "BOTH",
    "hour": "HOUR",
    "cascaded": "CASCADED",
    "scroll": "SCROLL",
    "immediate": "IMMEDIATE",
    "second": "SECOND",
    "cast": "CAST",
    "section": "SECTION",
    "catalog": "CATALOG",
    "include": "INCLUDE",
    "char": "CHAR",
    "session": "SESSION",
    "char_length": "CHAR_LENGTH",
    "character": "CHARACTER",
    "initially": "INITIALLY",
    "character_length": "CHARACTER_LENGTH",
    "size": "SIZE",
    "input": "INPUT",
    "smallint": "SMALLINT",
    "insensitive": "INSENSITIVE",
    "space": "SPACE",
    "int": "INT",
    "sql": "SQL",
    "collation": "COLLATION",
    "integer": "INTEGER",
    "sqlca": "SQLCA",
    "sqlcode": "SQLCODE",
    "sqlerror": "SQLERROR",
    "connect": "CONNECT",
    "sqlstate": "SQLSTATE",
    "connection": "CONNECTION",
    "sqlwarning": "SQLWARNING",
    "isolation": "ISOLATION",
    "substring": "SUBSTRING",
    "constraints": "CONSTRAINTS",
    "sum": "SUM",
    "language": "LANGUAGE",
    "corresponding": "CORRESPONDING",
    "last": "LAST",
    "temporary": "TEMPORARY",
    "count": "COUNT",
    "leading": "LEADING",
    "level": "LEVEL",
    "timestamp": "TIMESTAMP",
    "time": "TIME",
    "timezone_hour": "TIMEZONE_HOUR",
    "timezone_minute": "TIMEZONE_MINUTE",
    "local": "LOCAL",
    "lower": "LOWER",
    "match": "MATCH",
    "trailing": "TRAILING",
    "max": "MAX",
    "min": "MIN",
    "translate": "TRANSLATE",
    "date": "DATE",
    "minute": "MINUTE",
    "month": "MONTH",
    "true": "TRUE",
    "dec": "DEC",
    "names": "NAMES",
    "decimal": "DECIMAL",
    "natural": "NATURAL",
    "unknown": "UNKNOWN",
    "nchar": "NCHAR",
    "deferrable": "DEFERRABLE",
    "next": "NEXT",
    "upper": "UPPER",
    "deferred": "DEFERRED",
    "no": "NO",
    "usage": "USAGE",
    "none": "NONE",
    "describe": "DESCRIBE",
    "numeric": "NUMERIC",
    "varchar": "VARCHAR",
    "disconnect": "DISCONNECT",
    "octet_length": "OCTET_LENGTH",
    "only": "ONLY",
    "whenever": "WHENEVER",
    "work": "WORK",
    "value": "VALUE",
    "descriptor": "DESCRIPTOR",
    "domain": "DOMAIN",
    "write": "WRITE",
    "output": "OUTPUT",
    "zone": "ZONE",
    "translation": "TRANSLATION"
}

tokens = [
    # + - * / % ^
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "POWER",
    # ( ) [ ] { }
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    # = '!= | <>' < <= > >=
    "EQUAL",
    "NOT_EQUAL",
    "LESS_THAN",
    "LESS_EQUAL",
    "GREATER_THAN",
    "GREATER_EQUAL",
    # Identifiers and literals
    "ID",
    "STRING",
    # , ; .
    "COMMA",
    "SEMICOLON",
    "DOT",
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_POWER = r'\^'
t_ignore = ' \t'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_EQUAL = r'='
t_NOT_EQUAL = r'(!=)|(<>)'
t_LESS_THAN = r'<'
t_LESS_EQUAL = r'<='
t_GREATER_THAN = r'>'
t_GREATER_EQUAL = r'>='

t_STRING = r"'[^']*(''[^']*)*'"

t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*|\[[^\]]+\]'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT_LINE(t):
    r'--[^\n]*'
    pass

def t_COMMENT_MULTILINE(t):
    r'/\*(.|\n)*?\*/'
    pass

collumn = -1

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    global collumn
    collumn = t.lexer.lexpos - 1

def t_error(t):
   print("Illegal character '%s'" % t.value[0], ', line:', t.lineno, ', column: ', t.lexpos - collumn)
   t.lexer.skip(1)

def main():
    file = open("test.sql", "r")
    lexer = lex.lex()
    lexer.input(file.read())
    print('\n# lexer output:\n')
    for tok in lexer:
        print('type:', tok.type, ', value:', tok.value, ', line:', tok.lineno, ', column: ', tok.lexpos - collumn)
    print()

if __name__ == "__main__":
    main()
