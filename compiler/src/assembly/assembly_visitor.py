import compiler.src.assembly.symbol_table_asm as st_asm
import compiler.src.semantic.semantic_visitor as sv
from compiler.src.schema.schema import Schema
from compiler.src.visitor.visitor import *
from os.path import getsize

class AssemblyVisitor(AbstractVisitor):

    def __init__(self, nome_banco, nome_schema):
        st_asm.beginScope(st_asm.SCOPE_MAIN)
        self.funcs = []
        self.text = ['\n.text', '    move $fp, $sp']
        self.data = set([
                            ('mensagem_arquivo_dir_sucesso', '.asciiz "Recurso deletado com sucesso!\\n\\n"'), ('mensagem_arquivo_dir_falha', '.asciiz "Recurso não deletado.\\n\\n"'), 
                            ('mensagem_sucesso_create_dir', '.asciiz "Recurso criado com sucesso!\\n\\n"'), ('mensagem_falha_create_dir', '.asciiz "Recurso não criado!\\n\\n"'), 
                            ('log_file', f'.asciiz "transactions.log"')
                            ])
        self.rotulos = {}
        self.tamanho_buffer = 1024

        self.acoes_log = [] # Cada registro é composto por 'TIPO, OBJETO, CAMINHO, OBSERVACAO'
        self.nome_banco = nome_banco
        self.nome_schema = nome_schema
        self.caminho_arquivo_base = f'databases/{self.nome_banco}/schemes/{self.nome_schema}/tables'
        self.table_atual = None
        self.limpar_dados = False # Flag para indicar se a função de deletar todas as linhas deve ser criada
        self.contador_funcoes = 1

    def visitEmptyScript(self, _):
        return

    def visitCompoundScript(self, command):
        command.command.accept(self)
        command.script.accept(self)

    def visitTruncate(self, command):
        st_asm.beginScope('truncate')
        table = command.table.name.lower()
        st_asm.addCommand('truncate', table=table)
        caminho_tb = f'{self.caminho_arquivo_base}/{table}/{table}.csv'
        with open(f'compiler/resources/{caminho_tb}', 'r') as file:
            linha = file.readline().strip()
        
        var_tb = f'caminho_truncate_{table}_{self.contador_funcoes}'
        var_cabecalho = f'cabecalho_truncate_{table}_{self.contador_funcoes}'
        self.data.add((var_tb, f'.asciiz "{caminho_tb}"'))
        self.data.add((var_cabecalho, f'.asciiz "{linha}\\n"'))

        self.text.append(f'\n    # TRUNCATE na tabela {table}')
        self.text.append(f'    la $a0, {var_tb}')
        self.text.append(f'    la $a1, {var_cabecalho}')
        self.text.append(f'    li $a2, {len(linha) + 1}')
        self.text.append(f'    jal limpar_dados_tabela')
        
        self.limpar_dados = True
        self.contador_funcoes += 1
        st_asm.endScope()

    def visitCreateDatabase(self, command):
        st_asm.beginScope('create_database')
        nome_db = command.database.name.lower()
        st_asm.addCommand('create_db', database=nome_db)
        caminho_db = f'databases/{nome_db}/schemes/dbo'
        var_db = f'caminho_create_db_{nome_db}_{self.contador_funcoes}'

        self.data.add((var_db, f'.asciiz "{caminho_db}"'))  
        self.text.append(f'\n    # CREATE DATABASE - {nome_db}')
        self.text.append('    addi $sp, $sp, -4')
        self.text.append('    sw $ra, 0($sp)')
        self.text.append(f'    jal create_db_{self.contador_funcoes}')
        self.text.append('    lw $ra, 0($sp)') 
        self.text.append('    addi $sp, $sp, 4')
        st_asm.beginScope('create_db_sub')
        self.funcs.append(f'\ncreate_db_{self.contador_funcoes}:')
        self.funcs.append(f'    la $a0, {var_db}')
        self.funcs.append(f'    li $v0, 101')
        self.funcs.append(f'    syscall')
        self.funcs.append(f'    li $t0, 1')
        self.funcs.append(f'    beq $v0, $t0, print_sucesso_create_dir')
        self.funcs.append(f'    j print_falha_create_dir') 
        self.acoes_log.append(f'C, DATABASE, {caminho_db},')
        st_asm.endScope()
        
        self.contador_funcoes += 1
        st_asm.endScope()

    def visitDelete(self, delete):
        st_asm.beginScope('delete')
        table = delete.table.name.lower()
        
        if not delete.where:
            st_asm.addCommand('delete_all', table=table)
            caminho_tb = f'{self.caminho_arquivo_base}/{table}/{table}.csv'
            with open(f'compiler/resources/{caminho_tb}', 'r') as file:
                linha = file.readline().strip()

            var_tb = f'caminho_delete_all_{table}_{self.contador_funcoes}'
            var_cabecalho = f'cabecalho_delete_{table}_{self.contador_funcoes}'
            
            self.data.add((var_tb, f'.asciiz "{caminho_tb}"'))
            self.data.add((var_cabecalho, f'.asciiz "{linha}\\n"'))

            self.text.append(f'\n    # DELETE all na tabela {table}')
            self.text.append(f'    la $a0, {var_tb}')
            self.text.append(f'    la $a1, {var_cabecalho}')
            self.text.append(f'    li $a2, {len(linha) + 1}')
            self.text.append(f'    jal limpar_dados_tabela')
            
            self.limpar_dados = True
            self.contador_funcoes += 1
        else:
            pass

        st_asm.endScope()

        
    def visitDropDatabase(self, command):
        command.database.accept(self)
        database = command.database.name.lower()
        st_asm.addCommand('drop_db', database=database)
        var_db = f'caminho_db_{database}_{self.contador_funcoes}'
        caminho_db = f'databases/{database}'
        self.data.add((var_db, f'.asciiz "{caminho_db}"'))
        code = self.getList()
        code.append(f'\n    # Deletar banco {database}')
        code.append('    addi $sp, $sp, -8')
        code.append('    sw $ra, 0($sp)')
        code.append('    sw $fp, 4($sp)')
        code.append(f'    jal drop_db_{self.contador_funcoes}')
        code.append('    lw $fp, 4($sp)')
        code.append('    lw $ra, 0($sp)')
        code.append('    addi $sp, $sp, 8')
        st_asm.beginScope('drop_db')
        code = self.getList()
        code.append(f'drop_db_{self.contador_funcoes}:')
        code.append(f'    move $fp, $sp')
        code.append(f'    la $a0, {var_db}')
        code.append(f'    li $v0, 100           # Syscall RemoveDir')
        code.append(f'    syscall')
        code.append(f'    li $t0, 1')
        code.append(f'    beq $v0, $t0, print_sucesso_rm_dir')
        code.append(f'    j print_falha_rm_dir\n')
        self.acoes_log.append(f'D, DATABASE, {caminho_db},') 
        st_asm.endScope()
        self.contador_funcoes += 1

    def visitDropTable(self, command):
        table = command.table.name.lower()
        st_asm.addCommand('drop_table', table=table)
        var_arquivo = f'caminho_{self.nome_banco}_{self.nome_schema}_{table}'
        code = self.getList()
        code.append(f'\n    # Deletar da tabela {command.table.name}')
        code.append('    addi $sp, $sp, -8')
        code.append('    sw $ra, 0($sp)')
        code.append('    sw $fp, 4($sp)')
        code.append(f'    jal drop_table_{self.contador_funcoes}')
        code.append('    lw $fp, 4($sp)')
        code.append('    lw $ra, 0($sp)')
        code.append('    addi $sp, $sp, 8')
        st_asm.beginScope('select')
        command.table.accept(self)
        self.data.add((f'caminho_{self.nome_banco}_{self.nome_schema}_{table}', f'.asciiz "{self.caminho_arquivo_base}/{table}"'))
        code = self.getList()
        code.append(f'drop_table_{self.contador_funcoes}:')
        code.append(f'    move $fp, $sp')
        code.append(f'    la $a0, {var_arquivo}')
        code.append(f'    li $v0, 100  # RemoveDir')
        code.append(f'    syscall')
        code.append(f'    li $t0, 1')
        code.append(f'    beq $v0, $t0, print_sucesso_rm_dir')
        code.append(f'    j print_falha_rm_dir\n')
        self.acoes_log.append(f'D, TABLE, {self.caminho_arquivo_base}/{table},')
        st_asm.endScope()
        self.contador_funcoes += 1

        
    def visitSelect(self, select):
        self.text.append(f'\n    # SELECT na tabela {select.table.name}')    
        self.text.append(f'    jal select_{self.contador_funcoes}')
        st_asm.beginScope('select')
        self.table_atual = select.table.name.lower()
        st_asm.addCommand('select', table=self.table_atual)
        
        self.data.add((f'caminho_{self.nome_banco}_{self.nome_schema}_{self.table_atual}_select_{self.contador_funcoes}',
                      f'.asciiz "{self.caminho_arquivo_base}/{self.table_atual}/{self.table_atual}.csv"'))
        self.data.add(('conteudoArquivo', f'.space {self.tamanho_buffer}'))
        
        self.funcs.append(f'\nselect_{self.contador_funcoes}:')
        self.funcs.append(f'    addi $sp, $sp, -4')
        self.funcs.append(f'    sw $ra, 0($sp)')
        select.table.accept(self)
        select.columns.accept(self)        
        self.funcs.append(f'    lw $ra, 0($sp)')
        self.funcs.append(f'    addi $sp, $sp, 4')
        self.funcs.append(f'    jr $ra')
        st_asm.endScope()
        self.table_atual = None
        self.contador_funcoes += 1

    def visitSelectAll(self, select):
        code = self.getList()
        code.append(f'    li $v0, 13 # Abrir arquivo')
        code.append(
            f'    la $a0, caminho_{self.nome_banco}_{self.nome_schema}_{self.table_atual}_select_{self.contador_funcoes}')
        code.append(f'    li $a1, 0 # Modo leitura')
        code.append(f'    syscall\n')
        code.append(f'    move $s0, $v0')
        code.append(f'    move $a0, $s0')
        code.append(f'    li $v0, 14')
        code.append(f'    la $a1, conteudoArquivo')
        code.append(f'    li $a2, {self.tamanho_buffer - 1}')
        code.append(f'    syscall\n')
        code.append(f'    la $t0, conteudoArquivo')
        code.append(f'    add $t0, $t0, $v0')
        code.append(f'    sb $zero, 0($t0)')
        code.append(f'    li $v0, 4 # Imprimir arquivo')
        code.append(f'    la $a0, conteudoArquivo')
        code.append(f'    syscall\n')
        code.append(f'    li $v0, 16 # Fechar arquivo')
        code.append(f'    move $a0, $s0')
        code.append(f'    syscall\n')
        self.adicionar_quebra_linha(code)

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
        table = insert.table.name.lower()
        
        var_tb = f'caminho_insert_{table}_{self.contador_funcoes}'
        caminho_tb = f'{self.caminho_arquivo_base}/{table}/{table}.csv'
        self.data.add((var_tb, f'.asciiz "{caminho_tb}"'))
        
        novos_valores = ",".join([str(p.value) if hasattr(p, 'value') else str(p) for p in insert.parameters])
        var_novos = f'novos_valores_{self.contador_funcoes}'
        var_buffer = f'buffer_insert_{self.contador_funcoes}'
        
        self.data.add((var_buffer, f'.space {self.tamanho_buffer}'))
        self.data.add((var_novos, f'.asciiz "{novos_valores}\\n"'))

        code = self.getList()
        code.append(f'\n    # --- INSERT na tabela "{table}" ---')
        code.append('    addi $sp, $sp, -8')
        code.append('    sw $ra, 0($sp)')
        code.append('    sw $fp, 4($sp)')
        code.append(f'    jal insert_{self.contador_funcoes}')
        code.append('    lw $fp, 4($sp)')
        code.append('    lw $ra, 0($sp)')
        code.append('    addi $sp, $sp, 8')

        st_asm.beginScope('insert')
        st_asm.addCommand('insert', table=table, values=insert.parameters)
        code = self.getList()

        # Leitura
        code.append(f'\ninsert_{self.contador_funcoes}:')
        code.append('    addi $sp, $sp, -4')
        code.append('    sw $ra, 0($sp)')

        code.append('    li $v0, 13')
        code.append(f'    la $a0, {var_tb}')
        code.append('    li $a1, 0')
        code.append('    syscall')
        code.append('    move $s0, $v0')
        code.append('    li $v0, 14')
        code.append('    move $a0, $s0')
        code.append(f'    la $a1, {var_buffer}')
        code.append(f'    li $a2, {self.tamanho_buffer}')
        code.append('    syscall')
        code.append('    move $s1, $v0')
        code.append('    li $v0, 16')
        code.append('    move $a0, $s0')
        code.append('    syscall\n')

        # Junta os valores
        code.append(f'    la $a0, {var_buffer}')
        code.append(f'    la $a1, {var_novos}')
        code.append('    move $a2, $s1')
        code.append('    jal str_append')
        code.append('    move $s3, $v0\n')

        # Escrita
        code.append('    li $v0, 13')
        code.append(f'    la $a0, {var_tb}')
        code.append('    li $a1, 1')
        code.append('    syscall')
        code.append('    move $s0, $v0')
        code.append('    li $v0, 15')
        code.append('    move $a0, $s0')
        code.append(f'    la $a1, {var_buffer}')
        code.append('    move $a2, $s3')
        code.append('    syscall')
        code.append('    li $v0, 16')
        code.append('    move $a0, $s0')
        code.append('    syscall')

        code.append('    lw $ra, 0($sp)')
        code.append('    addi $sp, $sp, 4')
        code.append('    jr $ra')
        st_asm.endScope()
        self.contador_funcoes += 1

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

    def get_code(self):
        finalcode = []
        mensagem_log = "\\n".join(self.acoes_log) + "\\n" if self.acoes_log else ""
        if self.acoes_log:
            self.data.add(("mensagem_log", f'.asciiz "{mensagem_log}"'))
        if self.data:
            finalcode.append(".data")
            for label, valor in sorted(self.data):
                finalcode.append(f"    {label}: {valor}")
    
        finalcode.extend(self.text)

        if self.acoes_log:
            finalcode.append("\n    # Registrar log completo das operações")
            finalcode.append("    la $a1, mensagem_log")
            finalcode.append(f"    li $a2, {len(mensagem_log) - len(self.acoes_log)}")
            finalcode.append("    jal gravar_log")
        finalcode.append("\n    # Encerrar programa")
        finalcode.append("    j end")
        if self.limpar_dados:
            self.criar_funcao_limpa_dados()
        self.criar_funcoes_feedback()
        self.criar_funcao_log()
        self.criar_funcao_append()
        finalcode.extend(self.funcs)
        finalcode.append("\nend:")
        finalcode.append("    li $v0, 10")
        finalcode.append("    syscall")
        return "\n".join(finalcode)

    def adicionar_quebra_linha(self, code):
        code.append(f'    li $v0, 11')
        code.append(f'    li $a0, 10')
        code.append(f'    syscall\n')
        
    def criar_funcao_limpa_dados(self):
        self.funcs.append('\n# --- Limpar dados da tabela ---')
        self.funcs.append('limpar_dados_tabela:')
        self.funcs.append('    move $t0, $a0 ')
        self.funcs.append('    move $t1, $a1')
        self.funcs.append('    move $t2, $a2')
        self.funcs.append('    ')
        self.funcs.append('    li $v0, 13')
        self.funcs.append('    move $a0, $t0')
        self.funcs.append('    li $a1, 1')
        self.funcs.append('    li $a2, 0')
        self.funcs.append('    syscall')
        self.funcs.append('    move $t3, $v0')
        self.funcs.append('    ')
        self.funcs.append('    li $v0, 15')
        self.funcs.append('    move $a0, $t3')
        self.funcs.append('    move $a1, $t1')
        self.funcs.append('    move $a2, $t2')
        self.funcs.append('    syscall')
        self.funcs.append('    ')
        self.funcs.append('    li $v0, 16')
        self.funcs.append('    move $a0, $t3')
        self.funcs.append('    syscall')
        self.funcs.append('    jr $ra')

    def criar_funcoes_feedback(self):
        """Cria funções que apenas imprimem as mensagens e retornam"""
        self.funcs.append('\n# --- Feedback ---')
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

        self.funcs.append('\nprint_sucesso_create_dir:')
        self.funcs.append('    la $a0, mensagem_sucesso_create_dir')
        self.funcs.append('    li $v0, 4')
        self.funcs.append('    syscall')
        self.funcs.append('    jr $ra')
        
        self.funcs.append('\nprint_falha_create_dir:')
        self.funcs.append('    la $a0, mensagem_falha_create_dir')
        self.funcs.append('    li $v0, 4')
        self.funcs.append('    syscall')
        self.funcs.append('    jr $ra')

    def criar_funcao_log(self):
        self.funcs.append('\n# --- Gravação de Log ---')
        self.funcs.append('gravar_log:')
        self.funcs.append('    move $t8, $a1')
        self.funcs.append('    move $t9, $a2')
        self.funcs.append('    la $a0, log_file')
        self.funcs.append('    li $a1, 1')
        self.funcs.append('    li $v0, 13')
        self.funcs.append('    syscall')
        self.funcs.append('    move $a0, $v0')
        self.funcs.append('    move $a1, $t8')
        self.funcs.append('    move $a2, $t9')
        self.funcs.append('    li $v0, 15')
        self.funcs.append('    syscall')
        self.funcs.append('    li $v0, 16')
        self.funcs.append('    syscall')
        self.funcs.append('    jr $ra')

    def criar_funcao_append(self):
        self.funcs.append('\n# --- Concatena - $a1 no fim de $a0 --- ')
        self.funcs.append('str_append:')
        self.funcs.append('    add $t0, $a0, $a2')
        self.funcs.append('    move $t1, $a1')
        
        self.funcs.append('\nloop_append:')
        self.funcs.append('    lb $t2, 0($t1)')
        self.funcs.append('    beqz $t2, fim_append')
        self.funcs.append('    sb $t2, 0($t0)')
        self.funcs.append('    addi $t0, $t0, 1')
        self.funcs.append('    addi $t1, $t1, 1')
        self.funcs.append('    j loop_append')
        
        self.funcs.append('\nfim_append:')
        self.funcs.append('    sb $zero, 0($t0)')
        self.funcs.append('    sub $v0, $t0, $a0')
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
    print("\n# Arquivo assembly gerado com sucesso!\n")


if __name__ == "__main__":
    main('master', 'dbo')
