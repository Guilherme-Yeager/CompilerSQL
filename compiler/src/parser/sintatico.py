import compiler.src.ast.sintaxe_abstrata as sa
from compiler.src.lexer.lexer import *

def p_script_empty(p):
    'script : '
    p[0] = sa.EmptyScript()

def p_script_compound(p):
    'script : command SEMICOLON script'
    p[0] = sa.CompoundScript(p[1], p[3])

def p_command_truncate(p):
    'command : TRUNCATE TABLE object'
    p[0] = sa.Truncate(p[3])

def p_command_create_database(p):
    'command : CREATE DATABASE object'
    p[0] = sa.CreateDatabase(p[3])

# Outros

def p_type(p):
    '''type : INT
            | STRING'''
    p[0] = p[1]

def p_object_id(p):
    'object : ID'
    p[0] = p[1]

def p_object_schema(p):
    'object : ID DOT ID'
    p[0] = (p[1], p[3])

def p_object_db_schema(p):
    'object : ID DOT ID DOT ID'
    p[0] = (p[1], p[3], p[5])

def p_error(p):
    if p:
        print(f"Erro sintático no token: {p.value}")
    else:
        print("Erro sintático no final do arquivo")