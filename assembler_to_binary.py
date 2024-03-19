#Definición del diccionario de symbol_table
symbol_table = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN': 16384,
    'KBD': 24576
}
next_available_address = 16

def translate_a_instruction(instruction):
    global next_available_address # Declarar next_available_address como una variable global
    # Verifica si la instrucción es un número decimal
    if instruction.isdigit():
        decimal_value = int(instruction)
        binary_value = bin(decimal_value)[2:].zfill(16)
        return binary_value
    else:
        # La instrucción es una etiqueta o símbolo
        # Aquí deberías implementar la lógica para manejar las etiquetas y símbolos
        # según las convenciones del lenguaje Hack Assembler
        
        # Ejemplo: Si asumimos que todas las etiquetas/símbolos son variables y deben asignarse direcciones
        # de memoria secuenciales a partir de la dirección 16, podríamos hacer lo siguiente:
        
        # Primero, verifica si la etiqueta/símbolo ya está en el diccionario de conversiones
        if instruction in symbol_table:
            address = symbol_table[instruction]
        else:
            # La etiqueta/símbolo no está en el diccionario, así que asignamos una nueva dirección de memoria
            address = next_available_address
            symbol_table[instruction] = address
            next_available_address += 1
        
        binary_value = bin(address)[2:].zfill(16)
        return binary_value
    
def translate_comp(comp):
    comp_table = {
        # Mapea las partes de cálculo (comp) a su representación binaria
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        '!D': '0001101',
        '!A': '0110001',
        '-D': '0001111',
        '-A': '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
         'M': '1110000',
        'D-M': '1010011',
        'M+1': '1110111',
        'M-1': '1110010',
        'M-D': '1000111',
        'D+M': '1000010',
        '!M': '1110001',
        'D&M': '1000000', 
        'D|M': '1010101'
        # Agrega más mapeos según las convenciones del lenguaje Hack Assembler
    }

    if comp:
        return comp_table[comp]
    else:
        return ''  # Otra acción por defecto si comp está vacío

def translate_dest(dest):
    dest_table = {
        # Mapea las partes de destino (dest) a su representación binaria
        '': '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111'
        # Agrega más mapeos según las convenciones del lenguaje Hack Assembler
    }

    return dest_table[dest]


def translate_jump(jump):
    jump_table = {
        # Mapea las partes de salto (jump) a su representación binaria
        '': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
        # Agrega más mapeos según las convenciones del lenguaje Hack Assembler
    }

    return jump_table[jump]

def translate_c_instruction(instruction):
    binary_instruction = "111"

    # Separar las partes de la instrucción C
    dest = ""
    jump = ""
    comp = ""

    if "=" in instruction:
        dest, comp = instruction.split("=")
    if ";" in instruction:
        comp, jump = instruction.split(";")

    # Traducir las partes de la instrucción C a su representación binaria
    binary_instruction += translate_comp(comp)
    binary_instruction += translate_dest(dest)
    binary_instruction += translate_jump(jump)

    return binary_instruction

def translate_file(file_name):
    global next_available_address  # Declarar next_available_address como una variable global

    translations = []

    with open(file_name, "r") as file:
        for line in file:
            line = line.strip().split("//")[0]

            if line:
                if line.startswith("@"):
                    instruction = line[1:]
                    binary_instruction = translate_a_instruction(instruction)
                    translations.append((binary_instruction, f'@{instruction}'))
                else:
                    binary_instruction = translate_c_instruction(line)
                    translations.append((binary_instruction, line))

    return translations

# Llamada a la función translate_file con el nombre del archivo .asm
file_name = r'C:\Users\kenet\Desktop\Assembler\Rect.asm' # Debemos cambiar el nombre del archivo para poder realizar la traducción sin problemas
translations = translate_file(file_name)

# Imprimir las instrucciones traducidas
for binary_instruction, asm_instruction in translations:
    print(f"{binary_instruction}  // {asm_instruction}")
