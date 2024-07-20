import json
import os

def initialise():
    predefined = {
        "R0": "0", "R1": "1", "R2": "2", "R3": "3", "R4": "4", "R5": "5",
        "R6": "6", "R7": "7", "R8": "8", "R9": "9", "R10": "10", "R11": "11",
        "R12": "12", "R13": "13", "R14": "14", "R15": "15",
        "SCREEN": "16384", "KBD": "24576",
        "SP": "0", "LCL": "1", "ARG": "2", "THIS": "3", "THAT": "4"
    }

    # Define the directory and filename
    directory = "assembler"
    filename = "symbols.json"
    
    # Create the full path
    # filepath = os.path.join(directory, filename)
    # print(os.getcwd())
    os.chdir(directory)
    # print(os.getcwd())
    # Ensure the directory exists
    # os.makedirs(directory, exist_ok=True)
    
    if os.path.exists(filename):
        # File exists, read its contents
        with open(filename, "r") as infile:
            existing_data = json.load(infile)
        
        # Update existing data with predefined symbols if they don't exist
        for key, value in predefined.items():
            if key not in existing_data:
                existing_data[key] = value
        
        # Write the updated data back to the file
        with open(filename, "w") as outfile:
            json.dump(existing_data, outfile, indent=4)
    else:
        # File doesn't exist, create it with predefined symbols
        with open(filename, "w") as outfile:
            json.dump(predefined, outfile, indent=4)

    print(f"Symbols file '{filename}' has been initialised/updated.")

def main():
    pass

if __name__ == "__main__":
    initialise()
    main()