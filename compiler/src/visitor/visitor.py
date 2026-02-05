import ply.yacc as yacc
from compiler.src.visitor.abstract_visitor import AbstractVisitor
from compiler.src.visitor.aux_visitor_print import AuxVisitorPrint
from compiler.src.parser.sintatico import *


class Visitor(AbstractVisitor):

    def __init__(self):
        self.aux_printer = AuxVisitorPrint()

    def visitEmptyScript(self, _):
        return

    def visitCompoundScript(self, command):
        command.command.accept(self)
        self.aux_printer.pos_command += 1
        command.script.accept(self)

    def visitTruncate(self, command):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Truncate pos = {self.aux_printer.pos_command}>")
        self.aux_printer.add_output_sql(f"TRUNCATE TABLE ")
        command.table.accept(self)
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Truncate>")
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_sql(f";\n\n")

    def visitCreateDatabase(self, command):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<CreateDatabase pos = {self.aux_printer.pos_command}>")
        self.aux_printer.add_output_sql(f"CREATE DATABASE ")
        command.database.accept(self)
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</CreateDatabase>")
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_sql(f";\n\n")

    def visitDelete(self, delete):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Delete pos = {self.aux_printer.pos_command}>")
        self.aux_printer.add_output_sql(f"DELETE FROM ")
        delete.table.accept(self)
        if delete.where is not None:
            self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Where>")
            self.aux_printer.add_output_sql(f"\nWHERE ")
            delete.where.accept(self)
            self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Where>")
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Delete>")
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_sql(f";\n\n")

    def visitDropDatabase(self, command):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<DropDatabase pos = {self.aux_printer.pos_command}>")
        self.aux_printer.add_output_sql(f"DROP DATABASE ")
        command.database.accept(self)
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</DropDatabase>")
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_sql(f";\n\n")

    def visitDropTable(self, command):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<DropTable pos = {self.aux_printer.pos_command}>")
        self.aux_printer.add_output_sql(f"DROP TABLE ")
        command.table.accept(self)
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</DropTable>")
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_sql(f";\n\n")

    def visitSelect(self, select):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Select pos = {self.aux_printer.pos_command}>")
        self.aux_printer.add_output_sql(f"SELECT ")
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Object>{select.table.name}</Object>")
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Columns>")
        self.aux_printer.inc_tab()
        select.columns.accept(self)
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_sql(f" FROM {select.table.name};\n")
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Columns>")
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Select>")
        self.aux_printer.dec_tab()

    def visitSelectAll(self, _):
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<SelectAll/>")
        self.aux_printer.add_output_sql(f"*")

    def visitColumns(self, columns):
        columns_list = columns.columns_list
        for i, col in enumerate(columns_list):
            if i > 0:
                self.aux_printer.add_output_sql(", ")
            self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Column>")
            col.accept(self)
            self.aux_printer.dec_tab()
            self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Column>")

    def visitExpressionAri(self, expression):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<ExpressionAri>")
        expression.left.accept(self)
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Operator>{expression.operator}</Operator>")
        self.aux_printer.add_output_sql(f" {expression.operator} ")
        self.aux_printer.dec_tab()
        expression.right.accept(self)
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</ExpressionAri>")

    def visitFactorId(self, factor):
        self.aux_printer.inc_tab()
        partes = []
        if factor.db:
            partes.append(factor.db)
        if factor.schema:
            partes.append(factor.schema)
        partes.append(factor.name)
        nome_completo = ".".join(partes)
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Object>{nome_completo}</Object>")
        self.aux_printer.add_output_sql(f"{nome_completo}")
        

    def visitFactorInt(self, number):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Int>{number.value}</Int>")
        self.aux_printer.add_output_sql(f"{number.value}")

    def visitFactorString(self, string):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<String>{string.value}</String>")
        self.aux_printer.add_output_sql(f"{string.value}")

    def visitFactorGrouping(self, grouping):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Grouping>")
        self.aux_printer.add_output_sql(f"(")
        grouping.expression.accept(self)
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Grouping>")
        self.aux_printer.add_output_sql(f")")

    def visitExpressionComparison(self, expression):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<ExpressionComparison>")
        expression.left.accept(self)
        self.aux_printer.add_output_xml(f'{self.aux_printer.indent()}<Operator>"{expression.operator}"</Operator>')
        self.aux_printer.add_output_sql(f" {expression.operator} ")
        self.aux_printer.dec_tab()
        if expression.right is not None:
            expression.right.accept(self)
            self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</ExpressionComparison>")
        self.aux_printer.dec_tab()

    def visitExpressionBool(self, expression):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<ExpressionBool>")
        expression.left.accept(self)
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Operator>{expression.operator}</Operator>")
        self.aux_printer.add_output_sql(f" {expression.operator} ")
        expression.right.accept(self)
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</ExpressionBool>")
        self.aux_printer.dec_tab()

    def visitExpressionNullCheck(self, expression):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<ExpressionNullCheck>")
        expression.expression.accept(self)
        if expression.is_not:
            self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Operator>IS NOT NULL</Operator>")
            self.aux_printer.add_output_sql(f" IS NOT NULL")
        else:
            self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Operator>IS NULL</Operator>")
            self.aux_printer.add_output_sql(f" IS NULL")
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</ExpressionNullCheck>")
        self.aux_printer.dec_tab()
        
    
    def visitInsert(self, insert):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Insert pos = {self.aux_printer.pos_command}>")
        self.aux_printer.add_output_sql(f"INSERT INTO ")
        insert.table.accept(self)
        if insert.columns:
            self.aux_printer.add_output_sql(f" (")
            insert.columns.accept(self)
            self.aux_printer.add_output_sql(f")")
        self.aux_printer.add_output_sql(f"\nVALUES (")
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Parameters>")
        self.aux_printer.inc_tab()
        for i, param in enumerate(insert.parameters):
            if i > 0:
                self.aux_printer.add_output_sql(", ")
            self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Parameter>")
            param.accept(self)
            self.aux_printer.dec_tab()
            self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Parameter>")
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Parameters>")
        self.aux_printer.add_output_sql(f");\n\n")
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Insert>")
        self.aux_printer.dec_tab()
    
    def visitAssignmentUpdate(self, update):
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Item>")
        update.column.accept(self)
        self.aux_printer.add_output_sql(" = ")
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Assignment>=</Assignment>")
        self.aux_printer.dec_tab()
        update.value.accept(self)
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Item>")
        

    def visitUpdate(self, update):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Update = {self.aux_printer.pos_command}>")
        self.aux_printer.add_output_sql(f"UPDATE ")
        update.table.accept(self)
        self.aux_printer.add_output_sql(f" SET ")
        for i, item in enumerate(update.set_list):
            item.accept(self)
            if i < len(update.set_list) - 1:
                self.aux_printer.add_output_sql(", ")
        if update.where:
            self.aux_printer.add_output_sql(" WHERE ")
            update.where.accept(self)
        self.aux_printer.dec_tab()
        self.aux_printer.add_output_sql(f";\n\n")
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Update>")
        self.aux_printer.dec_tab()
        
    def visitCreateTable(self, command):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(
            f"{self.aux_printer.indent()}<CreateTable pos = {self.aux_printer.pos_command}>"
        )
        self.aux_printer.add_output_sql("CREATE TABLE ")

        command.table.accept(self)

        self.aux_printer.add_output_sql(" (\n")
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}<Columns>")
        self.aux_printer.inc_tab()

        for i, col in enumerate(command.columns):
            if i > 0:
                self.aux_printer.add_output_sql(",\n")
            col.accept(self)

        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(f"{self.aux_printer.indent()}</Columns>")
        self.aux_printer.add_output_sql("\n)")

        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(
            f"{self.aux_printer.indent()}</CreateTable>"
        )
        self.aux_printer.add_output_sql(";\n\n")

    def visitColumnDefinition(self, column):
        self.aux_printer.inc_tab()
        self.aux_printer.add_output_xml(
            f"{self.aux_printer.indent()}<ColumnDefinition>"
        )

        self.aux_printer.add_output_xml(
            f"{self.aux_printer.indent()}<Name>{column.name}</Name>"
        )
        self.aux_printer.add_output_sql(f"    {column.name} ")

        self.aux_printer.add_output_xml(
            f"{self.aux_printer.indent()}<Type>{column.type}</Type>"
        )
        self.aux_printer.add_output_sql(f"{column.type.upper()}")

        if column.size is not None:
            self.aux_printer.add_output_sql(f"({column.size})") 

        self.aux_printer.dec_tab()
        self.aux_printer.add_output_xml(
            f"{self.aux_printer.indent()}</ColumnDefinition>"
        )

    
def main(text_sql=None, mode_output=1):
    lexer = lex.lex()
    if text_sql:
        lexer.input(text_sql)
    else:
        file = open("compiler/test/test.sql", "r")
        lexer.input(file.read())
        file.close()
    parser = yacc.yacc()
    result = parser.parse(debug=False)
    visitor = Visitor()
    if result is not None:
        result.accept(visitor)
        visitor.aux_printer.mode = mode_output
        print("\n# Entrada:\n")
        visitor.aux_printer.generate_output()


if __name__ == "__main__":
    main()
