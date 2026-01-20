import compiler.src.sintaxe.sintaxe_abstrata as sa
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


def p_command_delete(p):
    'command : DELETE FROM object'
    p[0] = sa.Delete(p[3])


def p_command_delete_where(p):
    'command : DELETE FROM object WHERE expression'
    p[0] = sa.Delete(p[3], p[5])


def p_command_drop_database(p):
    'command : DROP DATABASE object'
    p[0] = sa.DropDatabase(p[3])


def p_command_drop_table(p):
    'command : DROP TABLE object'
    p[0] = sa.DropTable(p[3])


def p_command_select_all(p):
    'command : SELECT TIMES FROM object'
    p[0] = sa.Select(sa.SelectAll(), p[4])


def p_command_select(p):
    'command : SELECT columns FROM object'
    p[0] = sa.Select(p[2], p[4])

# Expressão


def p_expression(p):
    '''expression : expression_ari
                  | bool'''
    p[0] = p[1]

# Expressão aritmética


def p_expression_ari(p):
    '''expression_ari : expression_ari PLUS term
                      | expression_ari MINUS term
                      | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = sa.ExpressionAri(p[1], p[2], p[3])


def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = sa.ExpressionAri(p[1], p[2], p[3])

# Expressão booleana


def p_expression_bool_or(p):
    '''bool : bool OR bool_1
            | bool_1'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = sa.ExpressionBool(p[1], p[2], p[3])


def p_expression_bool_and(p):
    '''bool_1 : bool_1 AND bool_2
              | bool_2'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = sa.ExpressionBool(p[1], p[2], p[3])


def p_expression_bool_not(p):
    '''bool_2 : NOT bool_2
              | LPAREN bool RPAREN
              | comparison'''
    if len(p) == 3:
        p[0] = sa.ExpressionNot(p[2])
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_comparison(p):
    '''comparison : comparison comp_op comparison_1
                  | comparison_1'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = sa.ExpressionComparison(p[1], p[2], p[3])


def p_comparison_1(p):
    '''comparison_1 : comparison_1 eq_op comparison_2
                    | comparison_2'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = sa.ExpressionComparison(p[1], p[2], p[3])


def p_comparison_2(p):
    '''comparison_2 : factor null_op
                    | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = sa.ExpressionNullCheck(p[1], p[2] == "IS NOT NULL")


def p_null_op(p):
    '''null_op : IS NULL
               | IS NOT NULL'''
    p[0] = " ".join(p[1:])


def p_eq_op(p):
    '''eq_op : EQUAL
             | NOT_EQUAL'''
    p[0] = p[1]


def p_comp_op(p):
    '''comp_op : LESS_THAN
               | LESS_EQUAL
               | GREATER_THAN
               | GREATER_EQUAL'''
    p[0] = p[1]

# Fator


def p_factor_id(p):
    'factor : ID'
    p[0] = sa.FactorId(p[1])


def p_factor_int(p):
    'factor : INT'
    p[0] = sa.FactorInt(p[1])


def p_factor_string(p):
    'factor : STRING'
    p[0] = sa.FactorString(p[1])


def p_factor_grouping(p):
    'factor : LPAREN expression_ari RPAREN'
    p[0] = sa.FactorGrouping(p[2])

# Outros


def p_object_id(p):
    'object : ID'
    p[0] = sa.FactorId(p[1])


def p_object_schema(p):
    'object : ID DOT ID'
    p[0] = sa.FactorId(p[3], p[1])


def p_object_db_schema(p):
    'object : ID DOT ID DOT ID'
    p[0] = sa.FactorId(p[5], p[3], p[1])


def p_columns_multiple(p):
    '''columns : columns COMMA object'''
    p[1].columns_list.append(p[3])
    p[0] = p[1]


def p_columns(p):
    '''columns : object'''
    p[0] = sa.Columns([p[1]])


def p_error(p):
    if p:
        print(f"Erro sintático no token: {p.value} | Linha: {p.lineno}")
    else:
        print("Erro sintático no final do arquivo")
