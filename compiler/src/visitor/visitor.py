import ply.yacc as yacc
from compiler.src.visitor.abstract_visitor import AbstractVisitor
from compiler.src.parser.sintatico import *

class Visitor(AbstractVisitor):
    
    def __init__(self):
        self.pos_command = 1
        self.tab = 0

    def indent(self):
        return "   " * self.tab

    def inc_tab(self):
        self.tab += 1

    def dec_tab(self):
        self.tab -= 1

    def visitEmptyScript(self, _):
        return

    def visitCompoundScript(self, command):
        command.command.accept(self)
        self.pos_command += 1
        command.script.accept(self)

    def visitTruncate(self, command):
        self.inc_tab()
        print(f"{self.indent()}<Truncate pos = {self.pos_command}>")
        self.inc_tab()
        print(f"{self.indent()}<Table>{command.table}</Table>")
        self.dec_tab()
        print(f"{self.indent()}</Truncate>")
        self.dec_tab()

    def visitCreateDatabase(self, command):
        self.inc_tab()
        print(f"{self.indent()}<CreateDatabase pos = {self.pos_command}>")
        self.inc_tab()
        print(f"{self.indent()}<Database>{command.database}</Database>")
        self.dec_tab()
        print(f"{self.indent()}</CreateDatabase>")
        self.dec_tab()
    
    def visitDelete(self, delete):
        self.inc_tab()
        print(f"{self.indent()}<Delete pos = {self.pos_command}>") 
        self.inc_tab()
        print(f"{self.indent()}<Table>{delete.table}</Table>")
        if delete.where is not None:
            print(f"{self.indent()}<Where>")
            delete.where.accept(self)
            print(f"{self.indent()}</Where>")
        self.dec_tab()
        print(f"{self.indent()}</Delete>")
        self.dec_tab()
          
    def visitDropDatabase(self, cmd):
        self.inc_tab()
        print(f"{self.indent()}<DropDatabase pos = {self.pos_command}>")
        self.inc_tab()
        print(f"{self.indent()}<Database>{cmd.database}</Database>")
        self.dec_tab()
        print(f"{self.indent()}</DropDatabase>")
        self.dec_tab()
        
    def visitDropTable(self, cmd):
        print(f"{self.indent()}<DropTable pos = {self.pos_command}>")
        self.inc_tab()
        print(f"{self.indent()}<Table>{cmd.table}</Table>")
        self.dec_tab()
        print(f"{self.indent()}</DropTable>")    

    def visitExpressionAri(self, expression):
        print(f"{self.indent()}<ExpressionAri>")
        expression.left.accept(self)
        print(f"{self.indent()}<Operator>{expression.operator}</Operator>")
        self.dec_tab()
        expression.right.accept(self)
        self.dec_tab()
        print(f"{self.indent()}</ExpressionAri>")

    def visitFactorId(self, id):
        self.inc_tab()
        print(f"{self.indent()}<Id>{id.name}</Id>")

    def visitFactorInt(self, number):
        self.inc_tab()
        print(f"{self.indent()}<Int>{number.value}</Int>")

    def visitFactorString(self, string):
        self.inc_tab()
        print(f"{self.indent()}<String>{string.value}</String>")

    def visitFactorGrouping(self, grouping):
        self.inc_tab()
        print(f"{self.indent()}<Grouping>")
        self.inc_tab()
        grouping.expression.accept(self)
        self.dec_tab()
        print(f"{self.indent()}</Grouping>")
        self.dec_tab()
    
    def visitExpressionComparison(self, expression):
        self.inc_tab()
        print(f"{self.indent()}<ExpressionComparison>")
        expression.left.accept(self)
        print(f'{self.indent()}<Operator>"{expression.operator}"</Operator>')
        self.dec_tab()
        if expression.right is not None:
            expression.right.accept(self)
        self.dec_tab()
        print(f"{self.indent()}</ExpressionComparison>")
        self.dec_tab()
    
    def visitExpressionBool(self, expression):
        self.inc_tab()
        print(f"{self.indent()}<ExpressionBool>")
        expression.left.accept(self)
        print(f"{self.indent()}<Operator>{expression.operator}</Operator>")
        expression.right.accept(self)
        print(f"{self.indent()}</ExpressionBool>")
        self.dec_tab()
    
    def visitExpressionNullCheck(self, expression):
        self.inc_tab()
        print(f"{self.indent()}<ExpressionNullCheck>")
        expression.expression.accept(self)
        if expression.is_not:
            print(f"{self.indent()}<Operator>IS NOT NULL</Operator>")
        else:
            print(f"{self.indent()}<Operator>IS NULL</Operator>")
        self.dec_tab()
        print(f"{self.indent()}</ExpressionNullCheck>")
        self.dec_tab()

        

def main():
    file = open("compiler/test/test.sql", "r")
    lexer = lex.lex()
    lexer.input(file.read())
    parser = yacc.yacc()
    result = parser.parse(debug=False)
    print("\n# Entrada:\n")
    visitor = Visitor()
    print("<Script>")
    result.accept(visitor)
    print(r"<\Script>" + "\n")

if __name__ == "__main__":
    main()