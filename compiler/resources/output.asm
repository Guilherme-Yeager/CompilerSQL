.data
    buffer_insert_1: .space 1024
    caminho_insert_funcionario_1: .asciiz "databases/engs_ufs/schemes/biotlab/tables/funcionario/funcionario.csv"
    log_file: .asciiz "transactions.log"
    mensagem_arquivo_dir_falha: .asciiz "Recurso não deletado.\n\n"
    mensagem_arquivo_dir_sucesso: .asciiz "Recurso deletado com sucesso!\n\n"
    mensagem_falha_create_dir: .asciiz "Recurso não criado!\n\n"
    mensagem_sucesso_create_dir: .asciiz "Recurso criado com sucesso!\n\n"
    novos_valores_1: .asciiz "11,'Marcela','1033014382'\n"

.text
    move $fp, $sp

    # --- INSERT na tabela "funcionario" ---
    addi $sp, $sp, -8
    sw $ra, 0($sp)
    sw $fp, 4($sp)
    jal insert_1
    lw $fp, 4($sp)
    lw $ra, 0($sp)
    addi $sp, $sp, 8

    # Encerrar programa
    j end

insert_1:
    addi $sp, $sp, -4
    sw $ra, 0($sp)
    li $v0, 13
    la $a0, caminho_insert_funcionario_1
    li $a1, 0
    syscall
    move $s0, $v0
    li $v0, 14
    move $a0, $s0
    la $a1, buffer_insert_1
    li $a2, 1024
    syscall
    move $s1, $v0
    li $v0, 16
    move $a0, $s0
    syscall

    la $a0, buffer_insert_1
    la $a1, novos_valores_1
    move $a2, $s1
    jal str_append
    move $s3, $v0

    li $v0, 13
    la $a0, caminho_insert_funcionario_1
    li $a1, 1
    syscall
    move $s0, $v0
    li $v0, 15
    move $a0, $s0
    la $a1, buffer_insert_1
    move $a2, $s3
    syscall
    li $v0, 16
    move $a0, $s0
    syscall
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra

# --- Feedback ---
print_sucesso_rm_dir:
    la $a0, mensagem_arquivo_dir_sucesso
    li $v0, 4
    syscall
    jr $ra

print_falha_rm_dir:
    la $a0, mensagem_arquivo_dir_falha
    li $v0, 4
    syscall
    jr $ra

print_sucesso_create_dir:
    la $a0, mensagem_sucesso_create_dir
    li $v0, 4
    syscall
    jr $ra

print_falha_create_dir:
    la $a0, mensagem_falha_create_dir
    li $v0, 4
    syscall
    jr $ra

# --- Gravação de Log ---
gravar_log:
    move $t8, $a1
    move $t9, $a2
    la $a0, log_file
    li $a1, 1
    li $v0, 13
    syscall
    move $a0, $v0
    move $a1, $t8
    move $a2, $t9
    li $v0, 15
    syscall
    li $v0, 16
    syscall
    jr $ra

# --- Concatena - $a1 no fim de $a0 --- 
str_append:
    add $t0, $a0, $a2
    move $t1, $a1

loop_append:
    lb $t2, 0($t1)
    beqz $t2, fim_append
    sb $t2, 0($t0)
    addi $t0, $t0, 1
    addi $t1, $t1, 1
    j loop_append

fim_append:
    sb $zero, 0($t0)
    sub $v0, $t0, $a0
    jr $ra

end:
    li $v0, 10
    syscall