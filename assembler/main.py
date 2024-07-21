import json
import os
import parser
from translate import translateA
from translate import translateC

def initialise(DIR, SYM_FILE):
    predefined = {
        "R0": "0", "R1": "1", "R2": "2", "R3": "3", "R4": "4", "R5": "5",
        "R6": "6", "R7": "7", "R8": "8", "R9": "9", "R10": "10", "R11": "11",
        "R12": "12", "R13": "13", "R14": "14", "R15": "15",
        "SCREEN": "16384", "KBD": "24576",
        "SP": "0", "LCL": "1", "ARG": "2", "THIS": "3", "THAT": "4"
    }

    # Define the directory and filename
    # directory = "assembler"
    # SYM_FILE = "symbols.json"
    
    # Create the full path
    # filepath = os.path.join(directory, filename)
    # print(os.getcwd())
    # os.chdir(directory)
    # print(os.getcwd())
    # Ensure the directory exists
    # os.makedirs(directory, exist_ok=True)
    
    if os.path.exists(SYM_FILE):
        # File exists, read its contents
        with open(SYM_FILE, "r") as infile:
            existing_data = json.load(infile)
        
        # Update existing data with predefined symbols if they don't exist
        for key, value in predefined.items():
            if key not in existing_data:
                existing_data[key] = value
        
        # Write the updated data back to the file
        with open(SYM_FILE, "w") as outfile:
            json.dump(existing_data, outfile, indent=4)
    else:
        # File doesn't exist, create it with predefined symbols
        with open(SYM_FILE, "w") as outfile:
            json.dump(predefined, outfile, indent=4)

    print(f"Symbols file '{SYM_FILE}' has been initialised/updated.")

def parse(filename):
    c = parser.parser()
    c.labels(filename)
    c.variables(filename)

def translate(DIR, ASM_FILE, OUT_FILE, SYM_FILE):
    # chdir(DIR)
    filename = ASM_FILE
    OUTPUT_FILE = OUT_FILE
    symbols = SYM_FILE
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

if __name__ == "__main__":
    DIR = "assembler"
    ASM_FILE = "test.asm"
    OUT_FILE = "test.hack"
    SYM_FILE = "symbols.json"       # Do not change symbols.json file, unless you know what you are doing.

    initialise(DIR, SYM_FILE)
    parse(ASM_FILE)
    translate(DIR, ASM_FILE, OUT_FILE, SYM_FILE)
