from abc import abstractmethod, ABCMeta

class AbstractVisitor(metaclass=ABCMeta):

    @abstractmethod
    def visitEmptyScript(self, empty_script):
        pass

    @abstractmethod
    def visitCompoundScript(self, compound_script):
        pass

    @abstractmethod
    def visitTruncate(self, truncate_command):
        pass

    @abstractmethod
    def visitCreateDatabase(self, create_database_command):
        pass

    @abstractmethod
    def visitDelete(self, delete_command):
        pass

    @abstractmethod
    def visitDropDatabase(self, drop_database_command):
        pass

    @abstractmethod
    def visitDropTable(self, drop_table_command):
        pass

    @abstractmethod
    def visitExpressionComparison(self, expression):
        pass

    @abstractmethod
    def visitFactorId(self, id):
        pass

    @abstractmethod
    def visitFactorInt(self, number):
        pass
    
    @abstractmethod
    def visitFactorString(self, string):
        pass

    @abstractmethod
    def visitFactorGrouping(self, grouping):
        pass

    @abstractmethod
    def visitExpressionComparison(self, expression):
        pass

    @abstractmethod
    def visitExpressionBool(self, expression):
        pass

    @abstractmethod
    def visitExpressionNullCheck(self, expression):
        pass