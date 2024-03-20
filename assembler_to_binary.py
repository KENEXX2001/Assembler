#Proyecto #6 - Assembler to Binary

# El diccionario symbol_table contiene las asignaciones predefinidas de símbolos y direcciones de memoria.
# Cada clave representa un símbolo y su valor corresponde a la dirección de memoria asignada.
symbol_table = {
    'SP': 0,        # SP: Puntero de pila
    'LCL': 1,       # LCL: Puntero al segmento local
    'ARG': 2,       # ARG: Puntero al segmento de argumentos
    'THIS': 3,      # THIS: Puntero al segmento THIS
    'THAT': 4,      # THAT: Puntero al segmento THAT
    'SCREEN': 16384,    # SCREEN: Dirección base de la pantalla
    'KBD': 24576        # KBD: Dirección base del teclado
}

# next_available_address es una variable que indica la próxima dirección de memoria disponible para asignar a una etiqueta o símbolo.
# Inicialmente se establece en 16, ya que las direcciones de memoria anteriores están asignadas a los símbolos predefinidos.
next_available_address = 16

def translate_a_instruction(instruction):
    global next_available_address  # Declarar next_available_address como una variable global
    
    if instruction.isdigit():
        # Si la instrucción es un número decimal, se convierte a su representación binaria de 16 bits.
        decimal_value = int(instruction)
        binary_value = bin(decimal_value)[2:].zfill(16)
        return binary_value
    else:
        # Si la instrucción no es un número decimal, se asume que es una etiqueta o símbolo.
        # Si la etiqueta o símbolo ya está en el diccionario symbol_table, se obtiene la dirección asociada.
        # De lo contrario, se asigna una nueva dirección a la etiqueta o símbolo y se actualiza el diccionario.
        # La nueva dirección se toma de la variable next_available_address y se incrementa para la siguiente asignación.
        if instruction in symbol_table:
            address = symbol_table[instruction]
        else:
            address = next_available_address
            symbol_table[instruction] = address
            next_available_address += 1
        
        # La dirección se convierte a su representación binaria de 16 bits.
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

    translations = []  # Lista para almacenar las traducciones de las instrucciones

    with open(file_name, "r") as file:
        for line in file:
            line = line.strip().split("//")[0]  # Eliminar espacios en blanco y comentarios

            if line:
                if line.startswith("@"):
                    # Si la línea comienza con "@" es una instrucción A
                    instruction = line[1:]
                    binary_instruction = translate_a_instruction(instruction)
                    translations.append((binary_instruction, f'@{instruction}'))  # Agregar la traducción y la instrucción original a la lista
                else:
                    # Si no es una instrucción A, se asume que es una instrucción C
                    binary_instruction = translate_c_instruction(line)
                    translations.append((binary_instruction, line))  # Agregar la traducción y la instrucción original a la lista

    return translations

# Llamada a la función translate_file con el nombre del archivo .asm
file_name = r'C:\Users\kenet\Desktop\Assembler\Rect.asm' # Debemos cambiar el nombre del archivo para poder realizar la traducción sin problemas
translations = translate_file(file_name)

# Imprimir las instrucciones traducidas
for binary_instruction, asm_instruction in translations:
    print(f"{binary_instruction}  // {asm_instruction}")
