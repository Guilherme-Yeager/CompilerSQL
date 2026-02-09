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
    def visitSelect(self, select_command):
        pass

    @abstractmethod
    def visitSelectAll(self, select_all):
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
    def visitExpressionBool(self, expression):
        pass

    @abstractmethod
    def visitExpressionNullCheck(self, expression):
        pass

    @abstractmethod
    def visitColumns(self, columns):
        pass

    @abstractmethod
    def visitExpressionAri(self, expression):
        pass

    @abstractmethod
    def visitInsert(self, insert):
        pass

    @abstractmethod
    def visitAssignmentUpdate(self, update):
        pass

    @abstractmethod
    def visitUpdate(self, update):
        pass

    @abstractmethod
    def visitCreateTable(self, command):
        pass

    @abstractmethod
    def visitColumnDefinition(self, column):
        pass

    