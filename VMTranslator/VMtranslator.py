'''
Usage:
  $ ./VMtranslator.py <program.vm>
'''
import sys
import random
from Parser import parser
from CodeWriter import generateMemoryAccess
from CodeWriter import generateArithmetic


def code(instType, instArgs):

    if instType=="C_ARITHMETIC":
        assembly = generateArithmetic(instArgs[0])
    
    elif instType=="C_PUSH":
        assembly = generateMemoryAccess(instArgs[0], (instArgs[1])[0], (instArgs[1])[1])
    
    else:
        assembly = generateMemoryAccess(instArgs[0], (instArgs[1])[0], (instArgs[1])[1])
    return assembly

def removeComments(lineList):
    newList = []
    for line in lineList:
        if (line.strip()).startswith("//"):
            continue
        elif "//" in line:
            removedComms=line.split('//')[0].strip()
            newList.append(removedComms)
        elif line=="\n":
            continue
        else:
            newList.append(line.strip())
    return newList

def main():
    fdIn = open(sys.argv[1],'r')
    
    outputFilename = (sys.argv[1].split("."))[0] + ".asm"
    fdOut = open(outputFilename,'w')
    
    inFileRead = fdIn.readlines()
    inFileRead = removeComments(inFileRead)
    
    
    for instruction in inFileRead:
        # print(parser(instruction))
        instruction_type, instruction_arguments = parser(instruction)
        assembly_code = code(instruction_type, instruction_arguments)
        fdOut.write(assembly_code+'\n')
    
    fdIn.close()
    fdOut.close()

if __name__ =="__main__":
    main()
