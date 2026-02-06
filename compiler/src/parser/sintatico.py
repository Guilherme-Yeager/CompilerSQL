import compiler.src.sintaxe.sintaxe_abstrata as sa
from compiler.src.lexer.lexer import *


def p_script_empty(p):
    'script : '
    p[0] = sa.EmptyScript()


def p_script_compound(p):
    'script : command SEMICOLON script'
    p[0] = sa.CompoundScript(p[1], p[3])

# Truncate


def p_command_truncate(p):
    'command : TRUNCATE TABLE object'
    p[0] = sa.Truncate(p[3])


# Create database

def p_command_create_database(p):
    'command : CREATE DATABASE object'
    p[0] = sa.CreateDatabase(p[3])


# Delete

def p_command_delete(p):
    'command : DELETE FROM object'
    p[0] = sa.Delete(p[3])


def p_command_delete_where(p):
    'command : DELETE FROM object WHERE bool'
    p[0] = sa.Delete(p[3], p[5])


# Drop database

def p_command_drop_database(p):
    'command : DROP DATABASE object'
    p[0] = sa.DropDatabase(p[3])

# Create table

def p_command_create_table(p):
    'command : CREATE TABLE object LPAREN column_defs RPAREN'
    p[0] = sa.CreateTable(p[3], p[5])

# Create table com coluna única

def p_table_columns_single(p):
    'column_defs : column_def'
    p[0] = [p[1]]

# Create table múltiplas colunas

def p_table_columns_list(p):
    'column_defs : column_def COMMA column_defs'
    p[0] = [p[1]] + p[3]

# Definição de coluna

def p_column_def(p):
    'column_def : ID type column_nullability_opt column_identity_opt column_constraint_list_opt column_default_opt'
    p[0] = sa.ColumnDefinition(
        name=p[1],
        col_type=p[2],
        nullability=p[3],
        identity=p[4],
        constraints=p[5],
        default_value=p[6]
    )

# Restrições na criação da tabela

def p_column_nullability_not_null(p):
    'column_nullability_opt : NOT NULL'
    p[0] = 'NOT NULL'

def p_column_nullability_null(p):
    'column_nullability_opt : NULL'
    p[0] = 'NULL'

def p_column_nullability_empty(p):
    'column_nullability_opt : '
    p[0] = None

def p_column_identity(p):
    'column_identity_opt : IDENTITY LPAREN INT COMMA INT RPAREN'
    p[0] = (p[3], p[5])

def p_column_identity_empty(p):
    'column_identity_opt : '
    p[0] = None

def p_column_constraint_list(p):
    'column_constraint_list_opt : column_constraint column_constraint_list_opt'
    p[0] = [p[1]] + p[2]

def p_column_constraint_list_empty(p):
    'column_constraint_list_opt : '
    p[0] = []

def p_column_constraint_pk(p):
    'column_constraint : PRIMARY KEY'
    p[0] = 'PRIMARY KEY'

def p_column_constraint_unique(p):
    'column_constraint : UNIQUE'
    p[0] = 'UNIQUE'

def p_column_default(p):
    'column_default_opt : DEFAULT factor'
    p[0] = p[2]

def p_column_default_empty(p):
    'column_default_opt : '
    p[0] = None


# Definição de tipos

def p_type_int(p):
    'type : INT'
    p[0] = ('int', None)

def p_type_varchar(p):
    'type : VARCHAR LPAREN INT RPAREN'
    p[0] = ('varchar', p[3])


# Drop table


def p_command_drop_table(p):
    'command : DROP TABLE object'
    p[0] = sa.DropTable(p[3])


# Select

def p_command_select_all(p):
    'command : SELECT TIMES FROM object'
    p[0] = sa.Select(sa.SelectAll(), p[4])


def p_command_select(p):
    'command : SELECT columns FROM object'
    p[0] = sa.Select(p[2], p[4])


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
    '''comparison_2 : expression_ari null_op
                    | expression_ari'''
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

def p_factor_null(p):
    'factor : NULL'
    p[0] = sa.FactorNull(p[1])

def p_factor_int(p):
    'factor : INT'
    p[0] = sa.FactorInt(p[1])


def p_factor_string(p):
    'factor : STRING'
    p[0] = sa.FactorString(p[1])


def p_factor_grouping(p):
    'factor : LPAREN expression_ari RPAREN'
    p[0] = sa.FactorGrouping(p[2])

# Insert


def p_command_insert_columns(p):
    'command : INSERT INTO object LPAREN columns RPAREN VALUES LPAREN parameters RPAREN'
    p[0] = sa.Insert(p[3], p[9], p[5])


def p_command_insert(p):
    'command : INSERT INTO object VALUES LPAREN parameters RPAREN'
    p[0] = sa.Insert(p[3], p[6])


def p_parameters_single(p):
    'parameters : expression_ari'
    p[0] = [p[1]]


def p_parameters_multiple(p):
    'parameters : parameters COMMA expression_ari'
    p[0] = p[1] + [p[3]]

# Update


def p_update_where(p):
    'command : UPDATE object SET set_list WHERE bool'
    p[0] = sa.Update(p[2], p[4], p[6])

def p_update(p):
    'command : UPDATE object SET set_list'
    p[0] = sa.Update(p[2], p[4])

def p_set_list_single(p):
    'set_list : set_item'
    p[0] = [p[1]]

def p_set_list_multiple(p):
    'set_list : set_list COMMA set_item'
    p[0] = p[1] + [p[3]]

def p_set_item(p):
    'set_item : ID EQUAL factor'
    column = sa.FactorId(p[1])
    value = p[3] 
    p[0] = sa.AssignmentUpdate(column, value) 


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
        print(f"Erro sintático no token: {p.value} | Linha: {p.lineno}\n")
    else:
        print("Erro sintático no final do arquivo\n")