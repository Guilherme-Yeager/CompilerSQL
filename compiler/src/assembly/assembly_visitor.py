import compiler.src.assembly.symbol_table_asm as st_asm
import compiler.src.semantic.semantic_visitor as sv
from compiler.src.schema.schema import Schema
from compiler.src.visitor.visitor import *


class AssemblyVisitor(AbstractVisitor):

    def __init__(self, nome_banco, nome_schema):
        st_asm.beginScope(st_asm.SCOPE_MAIN)
        self.funcs = []
        self.text = ['\n.text', '    move $fp, $sp']
        self.data = set([('mensagem_arquivo_dir_sucesso', f'.asciiz "Recurso deletado com sucesso!"'), ('mensagem_arquivo_dir_falha', f'.asciiz "Recurso não deletado."')])
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
        command.database.accept(self)
        database = command.database.name.lower()
        st_asm.addCommand('drop_db', database=database)
        indice = st_asm.getContadorComandos()
        var_db = f'caminho_db_{database}_{indice}'
        caminho_db = f'databases/{database}'
        self.data.add((var_db, f'.asciiz "{caminho_db}"'))
        code = self.getList()
        code.append(f'\n    # Deletar banco {database}')
        code.append('    addi $sp, $sp, -8')
        code.append('    sw $ra, 0($sp)')
        code.append('    sw $fp, 4($sp)')
        code.append(f'    jal drop_db_{indice}')
        code.append('    lw $fp, 4($sp)')
        code.append('    lw $ra, 0($sp)')
        code.append('    addi $sp, $sp, 8')
        st_asm.beginScope('delete_db')
        code = self.funcs
        code.append(f'drop_db_{indice}:')
        code.append(f'    move $fp, $sp')
        code.append(f'    la $a0, {var_db}')
        code.append(f'    li $v0, 100           # Syscall RemoveDir')
        code.append(f'    syscall')
        code.append(f'    li $t0, 1')
        code.append(f'    beq $v0, $t0, print_sucesso_rm_dir')
        code.append(f'    j print_falha_rm_dir\n')
        
        st_asm.endScope()

    def visitDropTable(self, command):
        table = command.table.name.lower()
        st_asm.addCommand('delete', table=table)
        indice = st_asm.getContadorComandos()
        var_arquivo = f'caminho_{self.nome_banco}_{self.nome_schema}_{table}'
        code = self.getList()
        code.append(f'\n    # Deletar da tabela {command.table.name}')
        code.append('    addi $sp, $sp, -8')
        code.append('    sw $ra, 0($sp)')
        code.append('    sw $fp, 4($sp)')
        code.append(f'    jal delete_{indice}')
        code.append('    lw $fp, 4($sp)')
        code.append('    lw $ra, 0($sp)')
        code.append('    addi $sp, $sp, 8')
        st_asm.beginScope('select')
        command.table.accept(self)
        self.data.add((f'caminho_{self.nome_banco}_{self.nome_schema}_{table}', f'.asciiz "{self.caminho_arquivo_base}/{table}"'))
        code = self.getList()
        code.append(f'delete_{indice}:')
        code.append(f'    move $fp, $sp')
        code.append(f'    la $a0, {var_arquivo}')
        code.append(f'    li $v0, 100  # RemoveDir')
        code.append(f'    syscall')
        code.append(f'    li $t0, 1')
        code.append(f'    beq $v0, $t0, print_sucesso_rm_dir')
        code.append(f'    j print_falha_rm_dir\n')
        st_asm.endScope()

        
    def visitSelect(self, select):
        code = self.getList()
        code.append(f'\n    # SELECT na tabela {select.table.name}')    
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
        code.append(f'    syscall\n')

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
        finalcode.append("\n    # Encerrar programa")
        finalcode.append("    j end\n")
        self.criar_funcoes_feedback()
        finalcode.extend(self.funcs)
        finalcode.append("\nend:")
        finalcode.append("    li $v0, 10")
        finalcode.append("    syscall")

        return "\n".join(finalcode)
    
    def criar_funcoes_feedback(self):
        """Cria funções que apenas imprimem as mensagens e retornam"""
        self.funcs.append('# --- Sub-rotinas de Feedback ---')
        self.funcs.append('print_sucesso_rm_dir:')
        self.funcs.append('    la $a0, mensagem_arquivo_dir_sucesso')
        self.funcs.append('    li $v0, 4')
        self.funcs.append('    syscall')
        self.funcs.append('    jr $ra')

        self.funcs.append('\nprint_falha_rm_dir:')
        self.funcs.append('    la $a0, mensagem_arquivo_dir_falha')
        self.funcs.append('    li $v0, 4')
        self.funcs.append('    syscall')
        self.funcs.append('    jr $ra')


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
                f'\nForam encontrados {svisitor.n_errors} erros semânticos.')
            return
    asmvisitor = AssemblyVisitor(nome_banco, nome_schema)
    result.accept(asmvisitor)
    with open(f'compiler/resources/output.asm', 'w', encoding='utf-8') as file:
        file.write(asmvisitor.get_code())
    st_asm.clearSymbolTable()
    svisitor.schema.reset_catalogo()
    print("\n# Arquivo assembly gerado com sucesso!\n")


if __name__ == "__main__":
    main('master', 'dbo')
