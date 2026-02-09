import compiler.src.semantic.symbol_table_semantic as st_sem
from compiler.src.visitor.visitor import *
from compiler.src.schema.schema import Schema
from compiler.src.sintaxe.sintaxe_abstrata import FactorNull

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
        st_sem.beginScope('script')
        command.command.accept(self)
        self.printer.aux_printer.pos_command += 1
        command.script.accept(self)
        st_sem.endScope()

    def visitTruncate(self, command):
        st_sem.beginScope('truncate')
        st_sem.addCommand('truncate', table=command.table.name)
        command.table.accept(self)
        if not self.schema.existe_tabela(command.table.name):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (TRUNCATE)> : Tabela '{command.table.name}' não existe no schema.")
            self.n_errors += 1
        st_sem.endScope()

    def visitCreateDatabase(self, command):
        st_sem.beginScope('createDatabase')
        st_sem.addCommand('createDatabase', database=command.database.name)
        command.database.accept(self)
        if not command.database.db and not command.database.schema:
            nome_banco = command.database.name
            if self.schema.existe_banco(nome_banco):
                print(
                    f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (CREATE DATABASE)> : Banco de dados já existe.")
                self.n_errors += 1
            else:
                self.schema.create_database_catalogo(nome_banco)
        else:
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (CREATE DATABASE)> : Informe apenas o nome do banco de dados.")
            self.n_errors += 1
        
        st_sem.endScope()

    def visitDelete(self, delete):
        st_sem.beginScope('delete')
        delete.table.accept(self)
        if not self.schema.existe_tabela(delete.table.name):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (Delete)> : Tabela '{delete.table.name}' não existe no schema.")
            self.n_errors += 1
        else:
            if delete.where:
                st_sem.addCommand('delete', table=delete.table.name, clauses=delete.where)
                self.comando_atual = 'Delete'
                self.table_atual = delete.table.name
                delete.where.accept(self)
        self.comando_atual = ''
        self.table_atual = None
        st_sem.endScope()

    def visitDropDatabase(self, command):
        st_sem.beginScope('delete')
        st_sem.addCommand('dropDatabase', database=command.database.name)
        command.database.accept(self)
        nome_banco = command.database.name
        if self.schema.existe_banco(nome_banco):
            if not self.schema.drop_database_catalogo(nome_banco):
                print(
                    f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (DROP DATABASE)> : Não é possível remover o banco de dados '{nome_banco}'.")
                self.n_errors += 1
        else:
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (DROP DATABASE)> : Banco de dados '{nome_banco}' não existe.")
            self.n_errors += 1
        st_sem.endScope()

    def visitDropTable(self, command):
        st_sem.beginScope('delete')
        st_sem.addCommand('dropTable', table=command.table.name)
        command.table.accept(self)
        nome_tabela = command.table.name
        if not self.schema.existe_tabela(nome_tabela):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (DROP TABLE)> : Tabela '{nome_tabela}' não existe no schema.")
            self.n_errors += 1
        self.schema.drop_table_catalogo(nome_tabela)
        st_sem.endScope()

    def visitSelect(self, select):
        st_sem.beginScope('select')
        self.table_atual = select.table.name
        st_sem.addCommand('select', columns=select.columns, table=self.table_atual)
        select.table.accept(self)
        self.comando_atual = 'Select'
        select.columns.accept(self)
        self.table_atual = None
        st_sem.endScope()

    def visitSelectAll(self, select):
        if not self.schema.existe_tabela(self.table_atual):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (SELECT ALL)> : Tabela '{self.table_atual}' não existe no schema.")
            self.n_errors += 1
        self.table_atual = None
        self.comando_atual = ''

    def visitColumns(self, columns):
        if not self.schema.existe_tabela(self.table_atual):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} ({self.comando_atual})> : Tabela '{self.table_atual}' não existe no schema.")
            self.n_errors += 1
            return
        for column in columns.columns_list:
            if not self.schema.existe_coluna(self.table_atual, column.name):
                print(f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} ({self.comando_atual})> : "
                      f"Coluna '{column.name}' não existe na tabela '{self.table_atual}'.")
                self.n_errors += 1
                return
            column.accept(self)

    def visitExpressionAri(self, expression):
        tipo_esq = self.buscar_tipo_factor(expression.left)
        tipo_dir = self.buscar_tipo_factor(expression.right)
        if tipo_esq is None or tipo_dir is None:
            return None
        if tipo_esq != SemanticVisitor.TIPO_INT or tipo_dir != SemanticVisitor.TIPO_INT:
            print(f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} ({self.comando_atual})> : "
                f"Operação aritmética inválida entre {tipo_esq} e {tipo_dir}.")
            self.n_errors += 1

    def visitFactorId(self, factor):
        return SemanticVisitor.TIPO_OBJETO

    def visitFactorInt(self, number):
        return SemanticVisitor.TIPO_INT

    def visitFactorString(self, string):
        return SemanticVisitor.TIPO_STR

    def visitFactorGrouping(self, grouping):
        pass

    def visitExpressionComparison(self, expression):
        tipo_esq = self.buscar_tipo_factor(expression.left)
        tipo_dir = self.buscar_tipo_factor(expression.right)
        if tipo_esq is None or tipo_dir is None:
                return
        if tipo_esq != tipo_dir:
            print(f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} ({self.comando_atual})> : "
                f"Incompatibilidade de tipos: Comparação entre {tipo_esq} e {tipo_dir}")
            self.n_errors += 1

    def visitExpressionBool(self, expression):
        expression.left.accept(self)
        expression.right.accept(self)

    def visitExpressionNullCheck(self, expression):
        tipo = expression.expression.accept(self)
        if tipo == SemanticVisitor.TIPO_OBJETO:
            nome_coluna = expression.expression.name
            if not self.schema.existe_coluna(self.table_atual, nome_coluna):
                print(f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command}> ({self.comando_atual}) : "
                      f"Coluna '{nome_coluna}' não existe na tabela '{self.table_atual}'.")
                self.n_errors += 1

    def normalizar_tipo(self, tipo):
        if tipo is None:
            return None
        tipo = tipo.lower()
        if tipo.startswith("varchar") or tipo == SemanticVisitor.TIPO_STR:
            return SemanticVisitor.TIPO_STR
        if tipo == SemanticVisitor.TIPO_INT:
            return SemanticVisitor.TIPO_INT
        return tipo


    def visitInsert(self, insert):
        st_sem.beginScope('insert')

        insert.table.accept(self)
        self.table_atual = insert.table.name.lower()
        self.comando_atual = 'INSERT'

        if not self.schema.existe_tabela_insert(self.table_atual):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (INSERT)> : "
                f"Tabela '{self.table_atual}' não existe no schema."
            )
            self.n_errors += 1
            st_sem.endScope()
            return

        if insert.columns:
            colunas = []
            for col in insert.columns.columns_list:
                if not self.schema.existe_coluna(self.table_atual, col.name):
                    print(
                        f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (INSERT)> : "
                        f"Coluna '{col.name}' não existe na tabela '{self.table_atual}'."
                    )
                    self.n_errors += 1
                    st_sem.endScope()
                    return
                colunas.append(col.name)
        else:
            colunas = list(self.schema.schema[self.table_atual]["columns"].keys())

        valores = insert.parameters

        if len(colunas) != len(valores):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (INSERT)> : "
                f"Número de colunas diferente do número de valores."
            )
            self.n_errors += 1
            st_sem.endScope()
            return

        for coluna, valor in zip(colunas, valores):
            restricoes = self.schema.buscar_restricao_coluna(self.table_atual, coluna)

            if "not null" in restricoes and isinstance(valor, FactorNull):
                print(
                    f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (INSERT)> : "
                    f"Coluna '{coluna}' não aceita NULL."
                )
                self.n_errors += 1
                continue

            tipo_coluna = self.normalizar_tipo(
                self.schema.buscar_tipo_coluna(self.table_atual, coluna)
            )
            tipo_valor = self.normalizar_tipo(
                self.buscar_tipo_factor(valor)
            )

            if tipo_coluna != tipo_valor:
                print(
                    f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (INSERT)> : "
                    f"Tipo incompatível na coluna '{coluna}'."
                )
                self.n_errors += 1

        self.table_atual = None
        self.comando_atual = ''
        st_sem.endScope()


    def visitAssignmentUpdate(self, update):
        nome_coluna = update.column.name

        if not self.schema.existe_coluna(self.table_atual, nome_coluna):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (UPDATE)> : "
                f"Coluna '{nome_coluna}' não existe na tabela '{self.table_atual}'."
            )
            self.n_errors += 1
            return

        restricoes = self.schema.buscar_restricao_coluna(self.table_atual, nome_coluna)

        if "not null" in restricoes and isinstance(update.value, FactorNull):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (UPDATE)> : "
                f"Coluna '{nome_coluna}' não aceita NULL."
            )
            self.n_errors += 1
            return

        tipo_coluna = self.normalizar_tipo(
            self.schema.buscar_tipo_coluna(self.table_atual, nome_coluna)
        )
        tipo_valor = self.normalizar_tipo(
            self.buscar_tipo_factor(update.value)
        )

        if tipo_coluna != tipo_valor:
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (UPDATE)> : "
                f"Tipo incompatível na coluna '{nome_coluna}'."
            )
            self.n_errors += 1

    def visitUpdate(self, update):
        st_sem.beginScope('update')

        update.table.accept(self)
        self.table_atual = update.table.name.lower()
        self.comando_atual = 'UPDATE'

        if not self.schema.existe_tabela(self.table_atual):
            print(
                f"\n[Erro] <Comando #{self.printer.aux_printer.pos_command} (UPDATE)> : "
                f"Tabela '{self.table_atual}' não existe no schema."
            )
            self.n_errors += 1
            st_sem.endScope()
            return

        for assignment in update.set_list:
            assignment.accept(self)

        if update.where:
            update.where.accept(self)

        self.table_atual = None
        self.comando_atual = ''
        st_sem.endScope()


    def visitCreateTable(self, command):
        pass
    
    def visitColumnDefinition(self, column):
        pass

    def buscar_tipo_factor(self, factor):
        '''
        Busca o tipo real de factor.

        Args:
            factor: o útlimo factor analisado.

        Returns:
            str: O tipo do factor.
            None: Caso a coluna não exista na tabela atual.
        '''
        tipo = factor.accept(self)
        if tipo == SemanticVisitor.TIPO_OBJETO:
            nome_coluna = factor.name
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
    parser = yacc.yacc()
    result = parser.parse()
    svisitor = SemanticVisitor(schema)
    svisitor.printer.aux_printer.mode = mode_output
    if result is not None:
        result.accept(svisitor)
        print(f"\nForam encontrados {svisitor.n_errors} erros.")
    
if __name__ == "__main__":
    main()
