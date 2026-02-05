from abc import abstractmethod
from abc import ABCMeta

'''
    Script
'''


class Script(metaclass=ABCMeta):

    @abstractmethod
    def accept(self, visitor):
        pass


class EmptyScript(Script):

    def accept(self, visitor):
        return visitor.visitEmptyScript(self)


class CompoundScript(Script):

    def __init__(self, command, script):
        self.command = command
        self.script = script

    def accept(self, visitor):
        return visitor.visitCompoundScript(self)


'''
    Command
'''


class Command(metaclass=ABCMeta):

    @abstractmethod
    def accept(self, visitor):
        pass


'''
    Truncate
'''


class Truncate(Command):

    def __init__(self, table):
        self.table = table

    def accept(self, visitor):
        return visitor.visitTruncate(self)


'''
    Create Database
'''


class CreateDatabase(Command):

    def __init__(self, database):
        self.database = database

    def accept(self, visitor):
        return visitor.visitCreateDatabase(self)

class CreateTable:
    def __init__(self, table, columns):
        self.table = table
        self.columns = columns

    def accept(self, visitor):
        return visitor.visitCreateTable(self)

class ColumnDefinition:
    def __init__(self, name, col_type):
        self.name = name
        self.type = col_type

    def accept(self, visitor):
        return visitor.visitColumnDefinition(self)

'''
    Delete
'''


class Delete(Command):

    def __init__(self, table, where=None):
        self.table = table
        self.where = where

    def accept(self, visitor):
        return visitor.visitDelete(self)


'''
    Drop
'''


class DropDatabase(Command):

    def __init__(self, database):
        self.database = database

    def accept(self, visitor):
        return visitor.visitDropDatabase(self)


class DropTable(Command):
    def __init__(self, table):
        self.table = table

    def accept(self, visitor):
        return visitor.visitDropTable(self)


'''
    Select
'''


class SelectAll(Command):

    def accept(self, visitor):
        return visitor.visitSelectAll(self)


class Select(Command):
    def __init__(self, columns, table, where=None):
        self.columns = columns
        self.table = table
        self.where = where

    def accept(self, visitor):
        return visitor.visitSelect(self)


'''
    Expressão
'''


class Expression(metaclass=ABCMeta):

    @abstractmethod
    def accept(self, visitor):
        pass


'''
    Aritmética
'''


class ExpressionAri(Expression):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitExpressionAri(self)


'''
    Booleanas 
'''


class ExpressionBool(Expression):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitExpressionBool(self)


class ExpressionNot(Expression):

    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpressionNot(self)


class ExpressionComparison(Expression):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitExpressionComparison(self)


class ExpressionNullCheck(Expression):

    def __init__(self, expression, is_not=False):
        self.expression = expression
        self.is_not = is_not

    def accept(self, visitor):
        return visitor.visitExpressionNullCheck(self)


'''
    Fator
'''


class FactorId(Expression):
    def __init__(self, id_name, schema=None, db=None):
        self.name = id_name
        self.schema = schema
        self.db = db

    def accept(self, visitor):
        return visitor.visitFactorId(self)


class FactorInt(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitFactorInt(self)


class FactorString(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitFactorString(self)


class FactorNull(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitFactorString(self)


class FactorGrouping(Expression):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitFactorGrouping(self)


'''
     Insert
'''


class Insert(Command):
    def __init__(self, table, parameters, columns=None):
        self.table = table
        self.columns = columns
        self.parameters = parameters

    def accept(self, visitor):
        return visitor.visitInsert(self)


'''
    Update
'''


class Update(Command):

    def __init__(self, table, set_list, where=None):
        self.table = table
        self.set_list = set_list
        self.where = where

    def accept(self, visitor):
        return visitor.visitUpdate(self)


'''
    Outros
'''


class Columns(Expression):
    def __init__(self, columns_list):
        self.columns_list = columns_list

    def accept(self, visitor):
        return visitor.visitColumns(self)


'''
    Assignment
'''


class Assignment(metaclass=ABCMeta):

    @abstractmethod
    def accept(self, visitor):
        pass


class AssignmentUpdate(Assignment):
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def accept(self, visitor):
        return visitor.visitAssignmentUpdate(self)
