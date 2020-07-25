addi $t2, $zero, 10
sw $t2, 0($t2)
lw $t3, 0($t2)
beq $t3, $t2, -3
lw $t3, 0($t2)
slt $t0, $t4, $t3
sll $s1, $t0, 3
sub $s2, $s1, $s1