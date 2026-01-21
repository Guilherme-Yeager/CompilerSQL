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
        command.table.accept(self)
        self.dec_tab()
        print(f"{self.indent()}</Truncate>")
        self.dec_tab()

    def visitCreateDatabase(self, command):
        self.inc_tab()
        print(f"{self.indent()}<CreateDatabase pos = {self.pos_command}>")
        command.database.accept(self)
        self.dec_tab()
        print(f"{self.indent()}</CreateDatabase>")
        self.dec_tab()

    def visitDelete(self, delete):
        self.inc_tab()
        print(f"{self.indent()}<Delete pos = {self.pos_command}>")
        delete.table.accept(self)
        if delete.where is not None:
            print(f"{self.indent()}<Where>")
            delete.where.accept(self)
            print(f"{self.indent()}</Where>")
        self.dec_tab()
        print(f"{self.indent()}</Delete>")
        self.dec_tab()

    def visitDropDatabase(self, command):
        self.inc_tab()
        print(f"{self.indent()}<DropDatabase pos = {self.pos_command}>")
        command.database.accept(self)
        self.dec_tab()
        print(f"{self.indent()}</DropDatabase>")
        self.dec_tab()

    def visitDropTable(self, command):
        print(f"{self.indent()}<DropTable pos = {self.pos_command}>")
        command.table.accept(self)
        self.dec_tab()
        print(f"{self.indent()}</DropTable>")

    def visitSelect(self, select):
        self.inc_tab()
        print(f"{self.indent()}<Select pos = {self.pos_command}>")
        self.inc_tab()
        print(f"{self.indent()}<Object>{select.table.name}</Object>")
        print(f"{self.indent()}<Columns>")
        self.inc_tab()
        select.columns.accept(self)
        self.dec_tab()
        print(f"{self.indent()}</Columns>")
        self.dec_tab()
        print(f"{self.indent()}</Select>")
        self.dec_tab()

    def visitSelectAll(self, _):
        print(f"{self.indent()}<SelectAll/>")

    def visitColumns(self, columns):
        for col in columns.columns_list:
            print(f"{self.indent()}<Column>")
            col.accept(self)
            self.dec_tab()
            print(f"{self.indent()}</Column>")

    def visitExpressionAri(self, expression):
        print(f"{self.indent()}<ExpressionAri>")
        expression.left.accept(self)
        print(f"{self.indent()}<Operator>{expression.operator}</Operator>")
        self.dec_tab()
        expression.right.accept(self)
        self.dec_tab()
        print(f"{self.indent()}</ExpressionAri>")

    def visitFactorId(self, factor):
        self.inc_tab()
        partes = []
        if factor.db:
            partes.append(factor.db)
        if factor.schema:
            partes.append(factor.schema)
        partes.append(factor.name)
        nome_completo = ".".join(partes)
        print(f"{self.indent()}<Object>{nome_completo}</Object>")

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
        
    
    def visitInsert(self, insert):
        self.inc_tab()
        print(f"{self.indent()}<Insert pos = {self.pos_command}>")

        self.inc_tab()
        print(f"{self.indent()}<Table>")
        insert.table.accept(self)
        print(f"{self.indent()}</Table>")

        print(f"{self.indent()}<Parameters>")
        self.inc_tab()
        for param in insert.parameters:
            print(f"{self.indent()}<Parameter>")
            self.inc_tab()
            param.accept(self)
            self.dec_tab()
            print(f"{self.indent()}</Parameter>")
        self.dec_tab()
        print(f"{self.indent()}</Parameters>")

        self.dec_tab()
        print(f"{self.indent()}</Insert>")
        self.dec_tab()


def main(text_sql=None):
    lexer = lex.lex()
    if text_sql:
        lexer.input(text_sql)
    else:
        file = open("compiler/test/test.sql", "r")
        lexer.input(file.read())
        file.close()
    parser = yacc.yacc()
    result = parser.parse(debug=False)
    print("\n# Entrada:\n")
    visitor = Visitor()
    print("<Script>")
    result.accept(visitor)
    print(r"<\Script>" + "\n")


if __name__ == "__main__":
    main()
