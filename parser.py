from maps import instructions, registers, keywords, data_types
import os

avoid = [',', '[', ']', '{', '}', '(', ')', '+', '-']

while_map = {
    '>': 'jle',
    '<': 'jge',
    '>=': 'jl',
    '<=': 'jg',
    '==': 'jne'
}

user_defined = []
data_symbols = []
external_symbols = []

def compile_lines(lines):
    local_user_defined = user_defined.copy()
    local_data_symbols = {}
    output = ""
    current_section = "text"
    loop_counter = 0
    line_counter = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        line = line.split(";")[0]
        line_counter += 1
        try:
            for char in avoid:
                line = line.replace(char, f" {char} ")
            tokens = line.split()

            x = 0
            while x < len(tokens):
                token = tokens[x]
                print(token)
                if x == 0 and token == "section":
                    if tokens[x+1] == "data":
                        current_section = "data"
                        output += f"section {keywords['data']}"
                    else:
                        current_section = "text"

                if current_section == "text":
                    if token in instructions:
                        asm_name, argc = instructions[token]
                        output += asm_name + " "
                        args = [
                            tok for tok in tokens[x+1:x+1+argc+2]
                            if tok != ","
                        ][:argc]                    
                        if len(args) != argc:
                            raise Exception(f"{token} expects {argc} arguments but got {len(args)}")
                        
                    elif token in local_data_symbols:
                        output += token
                        
                    elif token in registers:
                        output += registers[token] + ''
                    elif token in keywords:
                        output += keywords[token] + ' '
                        if token == "global":
                            if x + 1 < len(tokens):
                                name = tokens[x+1]
                                if name in instructions:
                                    raise Exception(f"{name} is a reserved instruction name.")
                                local_user_defined.append(name)
                        
                        if token == "extern":
                            name = tokens[x+1]
                            if name in instructions or name in local_data_symbols:
                                raise Exception(f"{name} already defined")
                            external_symbols.append(name)
                    elif token == "for": #for [start] [end] [step]
                        loop_counter += 1
                        start = tokens[x+1]
                        end = tokens[x+2]
                        step = tokens[x+3]

                        body = []

                        j = i + 1
                        while j < len(lines):
                            next_line = lines[j].strip()

                            if next_line.strip().replace('\t', '') == "endfor":
                                break
                            body.append(next_line)
                            j += 1
                        
                        body_code = compile_lines(body)
                        body_intended = "\n".join(
                            "    " + line if line.strip() else line
                            for line in body_code.splitlines()
                        )
                        output += f"""
push rbx
mov rbx, {start}

.loop_{loop_counter}:
    cmp rbx, {end}
    jge .loop_{loop_counter}_end
{body_intended}
    add rbx, {step}
    jmp .loop_{loop_counter}

.loop_{loop_counter}_end:
    pop rbx
"""
                        x = len(tokens)
                        i = j + 1
                        break
                    elif token == "#macro": #macro [name] [param number]
                        macro_name = tokens[x+1]
                        param_num = tokens[x+2]
                        local_user_defined.append(macro_name)
                        body = []

                        j = i + 1
                        while j < len(lines):
                            next_line = lines[j].strip()
                            if next_line.strip().replace('\t', '') == "#endmac":
                                break
                            body.append(next_line)
                            j += 1
                        
                        body_code = compile_lines(body)
                        body_intended = "\n".join(
                            "    " + line if line.strip() else line
                            for line in body_code.splitlines()
                        )

                        output +=f"""
%macro {macro_name} {param_num}
{body_intended}
%endmacro
"""
                        x = len(tokens)
                        i = j + 1
                        break
                        
                    elif token == "while": #while [reg] [sign] [num]
                        loop_counter += 1
                        reg_name = tokens[x+1]
                        sign = tokens[x+2]
                        num = tokens[x+3]

                        if sign not in while_map:
                            raise Exception(f"Invalid condition sign for while loop.")
                        body = []
                        j = i + 1

                        while j < len(lines):
                            next_line = lines[j].strip()
                            if next_line.strip().replace('\t', '') == "endwhile":
                                break
                            body.append(next_line)
                            j += 1
                        body_code = compile_lines(body)
                        body_intended = "\n".join(
                            "    " + line if line.strip() else line
                            for line in body_code.splitlines()
                        )

                        output += f"""
.loop_{loop_counter}:
    cmp {registers[reg_name]}, {num}
    {while_map[sign]} .loop_{loop_counter}_end
{body_intended}
    jmp .loop_{loop_counter}
.loop_{loop_counter}_end:
"""
                        x = len(tokens)
                        i = j + 1
                        break
                    

                    elif token.isdigit() or (token.startswith("%") and token[1:].isdigit()):
                        output += token + " "
                    else:
                        if token.endswith(":") or token in local_user_defined or token in avoid or token in local_data_symbols or token in external_symbols:
                            output += token + ' ' 
                            if token.endswith(":"):
                                if token[:-1] in instructions or token[:-1] in external_symbols:
                                    raise Exception(f"{token[:-1]} is a reserved instruction name.")
                                local_user_defined.append(token[:-1])
                        else:
                            raise Exception(f"Unknown keyword: {token}")
                    x += 1
                elif current_section == "data":
                    if token == "#const": #const [name] [val]
                        var_name = tokens[x+1]
                        local_user_defined.append(var_name)
                        if tokens[x+2] == "strlen":
                            target = tokens[x+3]
                            if local_data_symbols[target] != "string":
                                raise Exception(f"'strlen' expects type 'string' but got type '{local_data_symbols[target]}'")
                            output += f"{var_name} equ $ - {target}"
                        else:
                            rest = " ".join(tokens[x+2:])
                            output += f"{var_name} equ {rest}"
                        break
                    
                    elif token == "#define":
                        var_name = tokens[x+1]
                        val = tokens[x+2]

                        local_user_defined.append(var_name)

                        output += f"%define {var_name} {val}"
                        break
                    elif token == "#assign":
                        var_name = tokens[x+1]
                        val = tokens[x+2]

                        local_user_defined.append(var_name)

                        output += f"%assign {var_name} {val}"
                        break
                    x += 1

                    parts = line.split()

                    if len(parts) <= 2:
                        continue

                    var_name = parts[0]
                    data_type = parts[1]

                    if data_type not in data_types and data_type != "string":
                        raise Exception(f"Unknown data type: {data_type}")
                    
                    local_data_symbols[var_name] = data_type
                    
                    if data_type == "string":
                        raw = " ".join(parts[2:]).strip()

                        if raw.startswith('"') and raw.endswith('"'):
                            raw = raw[1:-1]

                        output += f"{var_name} db \"{raw}\", 0 "
                        break
                    
                    else:
                        value = parts[2] if len(parts) > 2 else "0"
                        output += f"{var_name} {data_types[data_type]} {value} "
                        break

                        
        except Exception as e:
            print("FAILED LINE:", line_counter)
            print("LINE CONTENT:", lines[line_counter-1])
            print("ERROR:", repr(e))
            return None

        output = output.replace('[ ', '[').replace(' ]', ']').replace('( ', '(').replace(' )', ')').replace('{ ', '{').replace(' }', '}')
        output += '\n'

        i += 1

    return output

def parse_file(filename):

    with open(filename, 'r') as f:
        lines = f.readlines()
    
    output = compile_lines(lines)

    name = os.path.splitext(filename)[0]
    
    with open(f"{name}.asm", 'w') as f:
        f.write(output)

parse_file("examples/example.rasm")