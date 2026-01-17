import ply.lex as lex     #importa módulo ply.lex e o renomeia para lex

# Definindo Tokens e padroes
tokens = ("PLUS", "MINUS")
t_PLUS    = r'\+'
t_MINUS   = r'-'

# Criando Analisador Lexico, passando entrada
lexer = lex.lex()
lexer.input("+-- ++-")

# Realizando analise lexica
print('{:10s}{:10s}{:10s}{:10s}'.format("Token", "Lexema", "Linha", "Coluna"))
for tok in lexer:
  print('{:10s}{:10s}{:10s}{:10s}'.format(tok.type, tok.value, str(tok.lineno), str(tok.lexpos)))