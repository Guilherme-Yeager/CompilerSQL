import ply.yacc as yacc
from compiler.src.visitor.abstract_visitor import AbstractVisitor
from compiler.src.parser.sintatico import *

class Visitor(AbstractVisitor):
    
    def __init__(self):
        self.pos_command = 1

    def visitEmptyScript(self, _):
        return

    def visitCompoundScript(self, command):
        command.command.accept(self)
        self.pos_command += 1
        command.script.accept(self)

    def visitTruncate(self, command):
        print(f" <Truncate pos = {self.pos_command}>")
        print(f"    <Table>{command.table}</Table>")
        print(" </Truncate>")

    def visitCreateDatabase(self, command):
        print(f" <CreateDatabase pos = {self.pos_command}>")
        print(f"    <Database>{command.database}</Database>")
        print(" </CreateDatabase>")
    
    def visitDelete(self, delete):
        print(f" <Delete pos = {self.pos_command}>") 
        print(f"    <Table>{delete.table}</Table>")
        print(" </Delete>")   
          
    def visitDropDatabase(self, cmd):
        print(f" <DropDatabase pos = {self.pos_command}>")
        print(f"    <Database>{cmd.database}</Database>")
        print(" </DropDatabase")
        
    def visitDropTable(self, cmd):
        print(f" <DropTable pos = {self.pos_command}>")
        print(f"    <Table>{cmd.table}</Table>")
        print(" </DropTable")    

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