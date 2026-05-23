
%macro _add 2
    mov %1 , %2 
%endmacro


section .data
msg db "hello world", 0 

section .text 

SYS_EXIT equ $ - msg
global _start 

_start: 
mov rax, rcx

.loop_1:
    cmp rax, 10
    jg .loop_1_end
    inc rax
.loop_1_end:

ret 
