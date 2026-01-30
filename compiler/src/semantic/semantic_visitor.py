import compiler.src.semantic.symbol_table as st
from compiler.src.visitor.visitor import *
from compiler.src.schema.schema import Schema


class SemanticVisitor(AbstractVisitor):

    def __init__(self, schema):
        self.printer = Visitor()
        self.schema = schema
        self.n_errors = 0

    def visitEmptyScript(self, _):
        return

    def visitCompoundScript(self, command):
        st.beginScope('script')
        command.command.accept(self)
        st.endScope()

    def visitTruncate(self, command):
        st.beginScope('truncate')
        st.addCommand('truncate', table=command.table.name)
        command.table.accept(self)
        if not self.schema.existe_tabela(command.table.name):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (TRUNCATE)> : Tabela '{command.table.name}' não existe no schema.")
            self.n_errors += 1
        st.endScope()

    def visitCreateDatabase(self, command):
        st.beginScope('createDatabase')
        command.database.accept(self)
        if not command.database.db and not command.database.schema:
            nome_banco = command.database.name
            if self.schema.existe_banco(nome_banco):
                print(
                    f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (CREATE DATABASE)> : Banco de dados já existe.")
                self.n_errors += 1
        else:
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (CREATE DATABASE)> : Informe apenas o nome do banco de dados.")
            self.n_errors += 1
        st.endScope()

    def visitDelete(self, delete):
        pass

    def visitDropDatabase(self, command):
        pass

    def visitDropTable(self, command):
        pass

    def visitSelect(self, select):
        pass

    def visitSelectAll(self, _):
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


def main(text_sql=None, schema=None, mode_output=1):
    lexer = lex.lex()
    if text_sql:
        lexer.input(text_sql)
    else:
        file = open("compiler/test/test.sql", "r")
        lexer.input(file.read())
        file.close()
    if schema is None:
        schema = Schema()
    parser = yacc.yacc()
    result = parser.parse()
    svisitor = SemanticVisitor(schema)
    svisitor.printer.aux_printer.mode = mode_output
    if result is not None:
        result.accept(svisitor)
        print(f"\nForam encontrados {svisitor.n_errors} erros")


if __name__ == "__main__":
    main()
