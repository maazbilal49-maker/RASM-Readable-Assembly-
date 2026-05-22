instructions = {
    #move instructions
    "move": ('mov', 2),
    'move_zero': ('movzq', 2),

    #arithmatic instructions
    'add': ('add', 2),
    'sub': ('sub', 2),
    'mult': ('mul', 2),
    'div': ('div', 1),
    'xor': ('xor', 2),
    'or': ('or', 2),
    'and': ('and', 2),
    'not': ('not', 2),
    'test': ('test', 2),

    #push pop instructions
    'push': ('push', 1),
    'pop': ('pop', 1),

    #compare jump and return instructions
    'compare': ('cmp', 2),
    'jump': ('jmp', 1),
    'jump_if_greater': ('jg', 1),
    'jump_if_greater_equal': ('jge', 1),
    'jump_if_less': ('jl', 1),
    'jump_if_less_equal': ('jle', 1),
    'jump_if_equal':('je', 1),
    'jump_if_zero': ('jz', 1),
    "call": ("call", 1),
    'return': ('ret', 0)
}

registers = {
    #register A
    "reg_A_64": 'rax',
    'reg_A_32': 'eax',
    'reg_A_l16': 'ax',
    'reg_A_u8': 'ah',
    'reg_A_l8': 'al',

    #register B
    "reg_B_64": 'rbx',
    'reg_B_32': 'ebx',
    'reg_B_l16': 'bx',
    'reg_B_u8': 'bh',
    'reg_B_l8': 'bl',

    #register C
    "reg_C_64": 'rcx',
    'reg_C_32': 'ecx',
    'reg_C_l16': 'cx',
    'reg_C_u8': 'ch',
    'reg_C_l8': 'cl',

    #register D
    "reg_D_64": 'rdx',
    'reg_D_32': 'edx',
    'reg_D_l16': 'dx',
    'reg_D_u8': 'dh',
    'reg_D_l8': 'dl',

    #stack pointer
    "stack_pointer_64": 'rsp',
    'stack_pointer_32': 'esp',
    'stack_pointer_16': 'sp',

    #base pointer
    "base_pointer_64": 'rbp',
    'base_pointer_32': 'ebp',
    'base_pointer_16': 'bp',

    #source index register
    'reg_sourceindex_64': 'rsi',
    'reg_sourceindex_32': 'esi',
    'reg_sourceindex_16': 'si',
    'reg_sourceindex_8': 'sil',

    #destination index register
    'reg_destinationindex_64': 'rdi',
    'reg_destinationindex_32': 'edi',
    'reg_destinationindex_16': 'di',
    'reg_destinationindex_8': 'dil',
}

keywords = {
    "global": 'global',
    'extern': 'extern',
    'section': 'section',
    'text': '.text',
    'data': '.data',
    'double_word': 'DWORD',
    'quad_word': 'QWORD',
    'byte': 'byte',
    'ptr': 'ptr'
}

data_types = {
    "byte": "db",
    "word": "dw",
    "dword": "dd",
    "quad": "dq",
}