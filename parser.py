from maps import instructions, registers, keywords, data_types
import os

avoid = [',', '[', ']', '{', '}', '(', ')', '+', '-']

user_defined = []
data_symbols = []
external_symbols = []

def parse_file(filename):
    output = ""
    current_section = "text"

    with open(filename, 'r') as f:
        lines = f.readlines()
    line_counter = 0
    for line in lines:
        line = line.split(";")[0]
        line_counter += 1
        try:
            for char in avoid:
                line = line.replace(char, f" {char} ")
            tokens = line.split()

            for i, token in enumerate(tokens):
                if token == "section":
                    if tokens[i+1] == "data":
                        current_section = "data"
                        output += f"section {keywords['data']}"
                    else:
                        current_section = "text"

                if current_section == "text":
                    if token in instructions:
                        asm_name, argc = instructions[token]
                        output += asm_name + " "
                        args = [
                            tok for tok in tokens[i+1:i+1+argc+2]
                            if tok != ","
                        ][:argc]                    
                        if len(args) != argc:
                            raise Exception(f"{token} expects {argc} arguments but got {len(args)}")
                        
                    elif token in data_symbols:
                        output += token
                        
                    elif token in registers:
                        output += registers[token] + ''
                    elif token in keywords:
                        output += keywords[token] + ' '
                        if token == "global":
                            if i + 1 < len(tokens):
                                name = tokens[i+1]
                                if name in instructions:
                                    raise Exception(f"{name} is a reserved instruction name.")
                                user_defined.append(name)
                        
                        if token == "extern":
                            name = tokens[i+1]
                            if name in instructions or name in data_symbols:
                                raise Exception(f"{name} already defined")
                            external_symbols.append(name)

                    else:
                        if token.endswith(":") or token in user_defined or token in avoid or token in data_symbols or token in external_symbols:
                            output += token + ' ' 
                            if token.endswith(":"):
                                if token[:-1] in instructions or token[:-1] in external_symbols:
                                    raise Exception(f"{token[:-1]} is a reserved instruction name.")
                                user_defined.append(token[:-1])
                        else:
                            raise Exception(f"Unknown keyword: {token}")
                elif current_section == "data":
                    parts = line.split()

                    if len(parts) <= 2:
                        continue

                    var_name = parts[0]
                    data_type = parts[1]

                    data_symbols.append(var_name)

                    if data_type not in data_types and data_type != "string":
                        raise Exception(f"Unknown data type: {data_type}")
                    
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
            print(f"Error at line {line_counter}: {e}")
            return None

        output = output.replace('[ ', '[').replace(' ]', ']').replace('( ', '(').replace(' )', ')').replace('{ ', '{').replace(' }', '}')
        output += '\n'

    name = os.path.splitext(filename)[0]
    
    with open(f"{name}.asm", 'w') as f:
        f.write(output)