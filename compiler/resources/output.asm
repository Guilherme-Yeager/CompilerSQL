.data
    caminho_paciente: .asciiz "databases/engs_ufs/schemes/cuidado/tables/paciente/paciente.csv"
    conteudoArquivo: .space 1024

.text
    move $fp, $sp
    jal select_1
    j end

select_1:
    li $v0, 13 # Abrir arquivo
    la $a0, caminho_paciente
    li $a1, 0 # Modo leitura
    syscall

    move $s0, $v0
    move $a0, $s0
    li $v0, 14
    la $a1, conteudoArquivo
    li $a2, 1024
    syscall

    li $v0, 4 # Imprimir arquivo
    la $a0, conteudoArquivo
    syscall

    li $v0, 16 # Fechar arquivo
    move $a0, $s0
    syscall
    jr $ra

end:
    li $v0, 10
    syscall