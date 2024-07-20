import os
directory = "assembler"
os.chdir(directory)

import json

class parser:
    def __init__(self):
        self.filename = "test.asm"
        self.DEF = ["R0","R1","R2","R3","R4","R5","R6","R7","R8","R9","R10","R11","R12","R13","R14","R15", "SCREEN", "KBD", "SP", "LCL", "ARG", "THIS", "THAT"]
        self.LABLES = []
        self.VAR = []

    def addSymbol(filename, key, value):
        newSymbol = {key: value}
        # Read the existing data
        try:
            with open(filename, "r") as infile:
                existing_data = json.load(infile)
            
            # Update existing data with predefined symbols if they don't exist
            for key, value in newSymbol.items():
                if key not in existing_data:
                    existing_data[key] = value
            
            # Write the updated data back to the file
            with open(filename, "w") as outfile:
                json.dump(existing_data, outfile, indent=4)

        except FileNotFoundError:
            print("File Not Found.")
        except json.JSONDecodeError:
            print("Invalid JSON")

    def labels(self, filename):
        linenumber = -1
        flag = 0
        file = open(filename, "r")
        for line in file:
            strip_line = line.split('//')[0].strip()
            if not strip_line:
                continue
            if flag==0: 
                linenumber += 1
            flag = 0
            if strip_line.startswith("("):
                flag = 1
                symbol = strip_line[1:-1]
                parser.addSymbol("symbols.json", symbol, linenumber)
                print(f"Updated Label {symbol}")
                self.LABLES.append(symbol)
        file.close()

    def variables(self, filename):
        primaryADDR = 16
        linenumber = -1
        file = open(filename, "r")
        for line in file:
            strip_line = line.split('//')[0].strip()
            if not strip_line:
                continue
            linenumber += 1
            if strip_line.startswith("@"):
                symbol = strip_line[1:]
                if symbol not in self.LABLES:
                    if symbol not in self.DEF:
                        parser.addSymbol("symbols.json", symbol, primaryADDR)
                        print(f"Updated variable {symbol}")
                        self.VAR.append(symbol)
                        primaryADDR += 1


c = parser()
c.labels(filename = "test.asm")
c.variables(filename = "test.asm")