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