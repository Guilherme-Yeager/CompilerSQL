import compiler.src.assembly.symbol_table as st
from compiler.src.visitor.visitor import *

class AssemblyVisitor(AbstractVisitor):

    def __init__(self):
        st.beginScope(st.SCOPE_MAIN)
        self.funcs = []  
        self.text = [".text", "    move $fp, $sp"]
        self.data = set() 
        self.rotulos = {}

    def visitEmptyScript(self, _):
        pass

    def visitCompoundScript(self, command):
        pass

    def visitTruncate(self, command):
        pass

    def visitCreateDatabase(self, command):
        pass

    def visitDelete(self, delete):
        pass

    def visitDropDatabase(self, command):
        pass

    def visitDropTable(self, command):
        pass

    def visitSelect(self, select):
        pass

    def visitSelectAll(self, select):
        pass

    def visitColumns(self, columns):
        pass

    def visitExpressionAri(self, expression):
        pass

    def visitFactorId(self, factor):
        pass

    def visitFactorInt(self, number):
        pass

    def visitFactorString(self, string):
        pass

    def visitFactorGrouping(self, grouping):
        pass

    def visitExpressionComparison(self, expression):
        pass

    def visitExpressionBool(self, expression):
        pass

    def visitExpressionNullCheck(self, expression):
        pass

    def visitInsert(self, insert):
        pass

    def visitAssignmentUpdate(self, update):
        pass

    def visitUpdate(self, update):
        pass

    def getAssemblyType(type):
        if type == "string":
            return ".asciiz"
        return ".word"