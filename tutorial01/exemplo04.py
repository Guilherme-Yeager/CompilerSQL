import ply.lex as lex

# Definindo Tokens e seus padroes
tokens = ("PLUS", "MINUS", "ID", "NUMBER", "NUMBERFLOAT")
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_ID = r'[A-Za-z]+'
t_ignore  = ' \t'

def t_newline(t): #Adiciona a função t_newline
     r'\n+'
     t.lexer.lineno += len(t.value) #Atualiza o contador de linha a
                                    #depender da quantidade de \n
def t_NUMBERFLOAT(t):
     r'\d+\.\d+'
     t.value = float(t.value)  
     return t

def t_NUMBER(t):
     r'\d+'
     t.value = int(t.value)    
     return t

def t_error(t): 
  print("Caractere ilegal '%s'" %t.value[0]) 
  t.lexer.skip(1)


# Criando analisador Lexico e realizando analise lexica
lexer = lex.lex()
lexer.input("+  - --+ +  +\nestada 2.4 @ $")
for tok in lexer:
  print(tok.type, tok.value, tok.lineno, tok.lexpos)