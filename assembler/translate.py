import json
from os import chdir

dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

comp = {
    "0": {"a": "0", "c": "101010"},
    "1": {"a": "0", "c": "111111"},
    "-1": {"a": "0", "c": "111010"},
    "D": {"a": "0", "c": "001100"},
    "A": {"a": "0", "c": "110000"},
    "M": {"a": "1", "c": "110000"},
    "!D": {"a": "0", "c": "001101"},
    "!A": {"a": "0", "c": "110001"},
    "!M": {"a": "1", "c": "110001"},
    "-D": {"a": "0", "c": "001111"},
    "-A": {"a": "0", "c": "110011"},
    "-M": {"a": "1", "c": "110011"},
    "D+1": {"a": "0", "c": "011111"},
    "A+1": {"a": "0", "c": "110111"},
    "M+1": {"a": "1", "c": "110111"},
    "D-1": {"a": "0", "c": "001110"},
    "A-1": {"a": "0", "c": "110010"},
    "M-1": {"a": "1", "c": "110010"},
    "D+A": {"a": "0", "c": "000010"},
    "D+M": {"a": "1", "c": "000010"},
    "D-A": {"a": "0", "c": "010011"},
    "D-M": {"a": "1", "c": "010011"},
    "A-D": {"a": "0", "c": "000111"},
    "M-D": {"a": "1", "c": "000111"},
    "D&A": {"a": "0", "c": "000000"},
    "D&M": {"a": "1", "c": "000000"},
    "D|A": {"a": "0", "c": "010101"},
    "D|M": {"a": "1", "c": "010101"}
}

def decTObin(dec):
    bin_ = bin(int(dec))[2:].zfill(16)
    return bin_

def writeToHack(filename, line):
    # print("In WriteToHack")
    with open(filename, "a") as hack:
        hack.write(line+"\n")
    return 0

def translateA(line, Origin, Dest):
    # print("In TranslateA")

    instruction = line[1:]
    if instruction.isnumeric():
        instruction = int(instruction)
        machine = decTObin(instruction)
        return writeToHack(Dest, machine)

    try:
        with open(Origin, "r") as infile:
            content = infile.read()
            if content.strip():  # Check if file is not empty
                symbols = json.loads(content)
            else:
                print(f"Warning: The file {Origin} is empty.")
                symbols = {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {Origin}: {e}")
        symbols = {}
    except FileNotFoundError:
        print(f"Error: The file {Origin} was not found.")
        symbols = {}

    if instruction in symbols:
        value = symbols[instruction]
        machine = decTObin(value)
        return writeToHack(Dest, machine)

    else:
        return print("Failed to retrieve Symbols.")

def get_comp_bits(operation):
    if operation in comp:
        return comp[operation]["a"], comp[operation]["c"]
    else:
        return None, None

def get_dest_bits(operation):
    if operation in dest:
        return dest[operation]
    else:
        return None, None

def get_jump_bits(operation):
    if operation in jump:
        return jump[operation]
    else:
        return None, None

def translateC(line, Dest):
    # print("In TranslateC")

    line = line.strip()

    if ("=" in line) and (";" in line):
        dest = line.split("=")[0].strip()
        comp = line.split("=")[1].split(";")[0].strip()
        jump = line.split(";")[1].strip()

        a_bit, c_bits = get_comp_bits(comp)
        d_bits = get_dest_bits(dest)
        j_bits = get_jump_bits(jump)

    if ("=" in line) and (";" not in line):
        dest = line.split("=")[0].strip()
        comp = line.split("=")[1].strip()

        a_bit, c_bits = get_comp_bits(comp)
        d_bits = get_dest_bits(dest)
        j_bits = get_jump_bits("null")

    if ("=" not in line) and (";" in line):
        comp = line.split(";")[0].strip()
        jump = line.split(";")[1].strip()

        a_bit, c_bits = get_comp_bits(comp)
        d_bits = get_dest_bits("null")
        j_bits = get_jump_bits(jump)

    machine = "111" + a_bit + c_bits + d_bits + j_bits
    return writeToHack(Dest, machine)
        
if __name__ == "__main__":     
    chdir("assembler")
    filename = "test.asm"
    OUTPUT_FILE = "test.hack"
    symbols = "symbols.json"
    file = open(filename, "r")
    linenumber = -1
    for line in file:
        strip_line = line.split('//')[0].strip()
        if not strip_line:
            continue
        if strip_line.startswith("("):
            continue
        linenumber += 1
        
        # print(str(linenumber), strip_line)

        if strip_line.startswith("@"):
            translateA(strip_line, symbols, OUTPUT_FILE)
        else:
            translateC(strip_line, OUTPUT_FILE)
    print(f"Translated {linenumber}+1 lines in total.")