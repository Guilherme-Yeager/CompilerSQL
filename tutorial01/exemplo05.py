import ply.lex as lex

tokens = ('NUMBER', 'WORD', 'PLUS')
states = (('foo', 'exclusive'), ('bar', 'inclusive'))

t_WORD = r'[a-zA-Z]+'
t_ignore = ' \t'
t_foo_ignore = ' \t'
t_foo_NUMBER = r'\d+'  # Reconhece 'NUMBER' no estado 'foo'
t_foo_PLUS = r'\+'
t_bar_NUMBER = r'\d+'


def t_foo_newline(t):  #Reconhece quebra de linha no estado foo.
  r'\n'
  t.lexer.lineno += 1


def t_error(t):
  print('error in INITIAL state, %s' % t.value[0])
  t.lexer.skip(1)


def t_foo_error(t):
  print('error in foo state, %s' % t.value[0])
  t.lexer.skip(1)


def t_begin_foo(t):
  r'<foo>'
  t.lexer.begin('foo')

def t_foo_end_foo(t):
  r'\</foo\>'
  t.lexer.begin('INITIAL')

def t_bar_error(t):
  print('error in bar state, %s' % t.value[0])
  t.lexer.skip(1)

def t_begin_bar(t):
  r'<bar>'
  t.lexer.begin('bar')

def t_bar_end_bar(t):
  r'\</bar\>'
  t.lexer.begin('INITIAL')

lexer = lex.lex()
lex.input("lft  muito legal  <foo> 34423 + </foo> <bar> legal 51 2</bar>")
for l in lexer:
  print(l.value)