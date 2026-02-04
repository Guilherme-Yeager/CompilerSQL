import compiler.src.semantic.symbol_table as st
from compiler.src.visitor.visitor import *
from compiler.src.schema.schema import Schema


class SemanticVisitor(AbstractVisitor):

    TIPO_OBJETO = 'object'
    TIPO_INT = 'int'
    TIPO_STR = 'string'

    def __init__(self, schema):
        self.printer = Visitor()
        self.schema = schema
        self.table_atual = None
        self.comando_atual = ''
        self.n_errors = 0

    def visitEmptyScript(self, _):
        return

    def visitCompoundScript(self, command):
        st.beginScope('script')
        command.command.accept(self)
        self.printer.aux_printer.pos_command += 1
        command.script.accept(self)
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
        st.addCommand('createDatabase', database=command.database.name)
        command.database.accept(self)
        if not command.database.db and not command.database.schema:
            nome_banco = command.database.name
            if self.schema.existe_banco(nome_banco):
                print(
                    f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (CREATE DATABASE)> : Banco de dados já existe.")
                self.n_errors += 1
            self.schema.create_database_catalogo(nome_banco)
        else:
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (CREATE DATABASE)> : Informe apenas o nome do banco de dados.")
            self.n_errors += 1
        
        st.endScope()

    def visitDelete(self, delete):
        st.beginScope('delete')
        delete.table.accept(self)
        if not self.schema.existe_tabela(delete.table.name):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (Delete)> : Tabela '{delete.table.name}' não existe no schema.")
            self.n_errors += 1
        else:
            if delete.where:
                st.addCommand('delete', table=delete.table.name, clauses=delete.where)
                self.comando_atual = 'Delete'
                self.table_atual = delete.table.name
                delete.where.accept(self)
        self.comando_atual = ''
        self.table_atual = None
        st.endScope()

    def visitDropDatabase(self, command):
        st.beginScope('delete')
        st.addCommand('dropDatabase', database=command.database.name)
        command.database.accept(self)
        nome_banco = command.database.name
        if not self.schema.existe_banco(nome_banco):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (DROP DATABASE)> : Banco de dados '{nome_banco}' não existe.")
            self.n_errors += 1
        self.schema.drop_database_catalogo(nome_banco)
        st.endScope()

    def visitDropTable(self, command):
        st.beginScope('delete')
        st.addCommand('dropTable', table=command.table.name)
        command.table.accept(self)
        nome_tabela = command.table.name
        if not self.schema.existe_tabela(nome_tabela):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (DROP TABLE)> : Tabela '{nome_tabela}' não existe no schema.")
            self.n_errors += 1
        self.schema.drop_table_catalogo(nome_tabela)
        st.endScope()

    def visitSelect(self, select):
        pass

    def visitSelectAll(self, _):
        pass

    def visitColumns(self, columns):
        pass

    def visitExpressionAri(self, expression):
        pass

    def visitFactorId(self, factor):
        return SemanticVisitor.TIPO_OBJETO

    def visitFactorInt(self, number):
        return SemanticVisitor.TIPO_INT

    def visitFactorString(self, string):
        return SemanticVisitor.TIPO_STR

    def visitFactorGrouping(self, grouping):
        pass

    def visitExpressionComparison(self, expression):
        tipo_esq = self.buscar_tipo_coluna(expression.left)
        tipo_dir = self.buscar_tipo_coluna(expression.right)
        if tipo_esq is None or tipo_dir is None:
                return
        if tipo_esq != tipo_dir:
            print(f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} ({self.comando_atual})> : "
                f"Incompatibilidade de tipos: Comparação entre {tipo_esq} e {tipo_dir}")
            self.n_errors += 1

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

    def buscar_tipo_coluna(self, coluna):
        '''
        Busca o tipo real de uma coluna, antes validando
        se ela existe na tabela.

        Args:
            coluna: FactorId que é a coluna.

        Returns:
            str: O tipo da coluna.
            None: Caso a coluna não exista na tabela atual.
        '''
        tipo = coluna.accept(self)
        if tipo == SemanticVisitor.TIPO_OBJETO:
            nome_coluna = coluna.name
            if not self.schema.existe_coluna(self.table_atual, nome_coluna):
                print(f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command}> ({self.comando_atual}) : "
                      f"Coluna '{nome_coluna}' não existe na tabela '{self.table_atual}'.")
                self.n_errors += 1
                return None
            return self.schema.buscar_tipo_coluna(self.table_atual, nome_coluna)
        return tipo



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
        print(f"\nForam encontrados {svisitor.n_errors} erros.")


if __name__ == "__main__":
    main()
