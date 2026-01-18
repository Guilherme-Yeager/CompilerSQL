import ply.yacc as yacc
from compiler.src.visitor.abstract_visitor import AbstractVisitor
from compiler.src.parser.sintatico import *

class Visitor(AbstractVisitor):

    def visitEmptyScript(self, _):
        return

    def visitCompoundScript(self, command):
        command.command.accept(self)
        command.script.accept(self)

    def visitTruncate(self, command):
        print(" <Truncate>")
        print(f"    <Table>{command.table}</Table>")
        print(" </Truncate>")

    def visitCreateDatabase(self, command):
        print(" <CreateDatabase>")
        print(f"    <Database>{command.database}</Database>")
        print(" </CreateDatabase>")
    
    def visitDelete(self, delete):
        print("<delete>") 
        print(f" <Table>{delete.table}</Table>")
         
            
        print("</Delete>")     

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