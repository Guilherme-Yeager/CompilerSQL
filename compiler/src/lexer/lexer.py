import ply.lex as lex

reserved = {
    "truncate": "TRUNCATE",
    "table": "TABLE",
    "insert": "INSERT",
    "into": "INTO",
    "values": "VALUES",
    "select": "SELECT",
    "create": "CREATE",
    "from": "FROM",
    "where": "WHERE",
    "database": "DATABASE",
    "delete": "DELETE",
    "drop": "DROP",
    "update": "UPDATE",
    "set": "SET",
    "not": "NOT",
    "null": "NULL",
    "is": "IS",
    "int": "INT",
    "or": "OR",
    "and": "AND",
    "not": "NOT",
    
    # "default": "DEFAULT",
    # "primary": "PRIMARY",
    # "key": "KEY",
    # "unique": "UNIQUE",
    # "identity": "IDENTITY",
}


tokens = [
    # + - * / % ^
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    # "MOD",
    # "POWER",
    # ( ) [ ] { }
    "LPAREN",
    "RPAREN",
    # "LBRACKET",
    # "RBRACKET",
    # "LBRACE",
    # "RBRACE",
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
# t_MOD = r'%'
# t_POWER = r'\^'
t_ignore = ' \t'

t_LPAREN = r'\('
t_RPAREN = r'\)'
# t_LBRACKET = r'\['
# t_RBRACKET = r'\]'
# t_LBRACE = r'\{'
# t_RBRACE = r'\}'

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

def main(text_sql=None):
    lexer = lex.lex()
    if text_sql:
        lexer.input(text_sql)
    else:
        file = open("compiler/test/test.sql", "r")
        lexer.input(file.read())
        file.close()
    print('\n# Lexer output:\n')
    for tok in lexer:
        print('type:', tok.type, ', value:', tok.value, ', line:', tok.lineno, ', column: ', tok.lexpos - collumn)
    print()

if __name__ == "__main__":
    main()
