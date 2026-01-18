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
    
'''
    Delete
'''
    
class Delete(Command):
    def __init__(self, table):
        self.table = table

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
         self.table.table
        
    def accept(self, visitor):
         return visitor.visitDropTable(self)        
    
