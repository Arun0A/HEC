import json
from os import chdir

DEST_LINE = 0

def decTObin(dec):
    bin_ = bin(int(dec))[2:].zfill(16)
    return bin_

def writeToHack(filename, line):
    global DEST_LINE
    with open(filename, "a") as hack:
        if DEST_LINE == 0:
            hack.write(line)
            DEST_LINE = 1
        hack.write("\n" + line)

def translateA(line, Origin, Dest):
    instruction = line[1:]
    print(instruction)
    if instruction.isnumeric():
        instruction = int(instruction)
        machine = decTObin(instruction)
        writeToHack(Dest, machine)

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

    with open(Origin, "r") as infile:
        content = infile.read()
    print(f"File contents: {content}")

    if instruction in symbols:
        value = symbols[instruction]
        machine = decTObin(value)
        writeToHack(Dest, machine)

    else:
        print("Failed to retrieve Symbols.")

def translateC(line, filename):
    pass

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
    if strip_line.startswith("@"):
        translateA(strip_line, symbols, OUTPUT_FILE)
    else:
        translateC(strip_line, filename)