import compiler.src.assembly.symbol_table_asm as st_asm
import compiler.src.semantic.semantic_visitor as sv
from compiler.src.schema.schema import Schema
from compiler.src.visitor.visitor import *


class AssemblyVisitor(AbstractVisitor):

    def __init__(self, nome_banco, nome_schema):
        st_asm.beginScope(st_asm.SCOPE_MAIN)
        self.funcs = []
        self.text = ['\n.text', '    move $fp, $sp']
        self.data = set()
        self.rotulos = {}
        self.tamanho_buffer = 1024

        self.nome_banco = nome_banco
        self.nome_schema = nome_schema
        self.caminho_arquivo_base = f'databases/{self.nome_banco}/schemes/{self.nome_schema}/tables'
        self.table_atual = None

    def visitEmptyScript(self, _):
        return

    def visitCompoundScript(self, command):
        command.command.accept(self)
        command.script.accept(self)

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
        code = self.getList()
        code.append(f'    jal select_{st_asm.getContadorComandos()}')
        st_asm.beginScope('select')
        code = self.getList()
        code.append(f'select_{st_asm.getContadorComandos()}:')
        self.table_atual = select.table.name.lower()
        st_asm.addCommand('select', table=self.table_atual)
        select.table.accept(self)
        self.data.add((f'caminho_{self.nome_banco}_{self.nome_schema}_{self.table_atual}',
                      f'.asciiz "{self.caminho_arquivo_base}/{self.table_atual}/{self.table_atual}.csv"'))
        self.data.add(('conteudoArquivo', f'.space {self.tamanho_buffer}'))
        select.columns.accept(self)
        self.table_atual = None
        code.append(f'    jr $ra')
        st_asm.endScope()

    def visitSelectAll(self, select):
        code = self.getList()
        code.append(f'    li $v0, 13 # Abrir arquivo')
        code.append(
            f'    la $a0, caminho_{self.nome_banco}_{self.nome_schema}_{self.table_atual}')
        code.append(f'    li $a1, 0 # Modo leitura')
        code.append(f'    syscall\n')
        code.append(f'    move $s0, $v0')
        code.append(f'    move $a0, $s0')
        code.append(f'    li $v0, 14')
        code.append(f'    la $a1, conteudoArquivo')
        code.append(f'    li $a2, {self.tamanho_buffer}')
        code.append(f'    syscall\n')
        code.append(f'    li $v0, 4 # Imprimir arquivo')
        code.append(f'    la $a0, conteudoArquivo')
        code.append(f'    syscall\n')
        code.append(f'    li $v0, 16 # Fechar arquivo')
        code.append(f'    move $a0, $s0')
        code.append(f'    syscall')

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

    def visitCreateTable(self, command):
        pass

    def visitColumnDefinition(self, column):
        pass

    def getAssemblyType(type):
        if type == "string":
            return ".asciiz"
        return ".word"

    def getList(self):
        return self.text if st_asm.getScope() == f'{st_asm.SCOPE_MAIN}_1' else self.funcs

    # gera código assembly
    def get_code(self):
        finalcode = []
        if self.data:
            finalcode.append(".data")
            for label, valor in self.data:
                finalcode.append(f"    {label}: {valor}")
        finalcode.extend(self.text)
        finalcode.append("    j end\n")
        finalcode.extend(self.funcs)
        finalcode.append("\nend:")
        finalcode.append("    li $v0, 10")
        finalcode.append("    syscall")

        return "\n".join(finalcode)


def main(nome_banco, nome_schema, schema=Schema(), text_sql=None):
    lexer = lex.lex()
    if text_sql:
        lexer.input(text_sql)
    else:
        file = open("compiler/test/test.sql", "r")
        lexer.input(file.read())
        file.close()
    parser = yacc.yacc()
    result = parser.parse(debug=False)
    svisitor = sv.SemanticVisitor(schema)
    if result:
        result.accept(svisitor)
        if svisitor.n_errors > 0:
            print(
                f'\nForam encontrados {svisitor.n_errors} erros semânticos. O código assembly foi gerado.')
            return
    asmvisitor = AssemblyVisitor(nome_banco, nome_schema)
    result.accept(asmvisitor)
    with open(f'compiler/resources/output.asm', 'w', encoding='utf-8') as file:
        file.write(asmvisitor.get_code())
    st_asm.clearSymbolTable()
    print("\n# Arquivo assembly gerado com sucesso!\n")


if __name__ == "__main__":
    main('master', 'dbo')
