import sys
import random

function_calls = {}     # {"function_name": num_calls}

def generateArithmetic(command):
    counterJmp=str(random.randint(0,10000)) # get a random integer which we use to create unique conditional jump location
    
    if command == "add": 
        retStr= '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'M=D+M'
    elif command =="sub": 
        retStr= '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'M=D-M'
    elif command =='neg': 
        retStr= '@SP\n'+"M=M-1\n"+'A=M\n'+'M=-M\n'+'@SP\n'+'M=M+1'
    elif command =='and': 
        retStr = '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'M=D&M'
    elif command =='or': 
        retStr = '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'M=D|M'
    elif command =='not': 
        retStr= '@SP\n'+'M=M-1\n'+'A=M\n'+'M=!M\n'+'@SP\n'+'M=M+1'
    
    #For following conditional jumps we have have two locations JUMPTRUE and ENDJUMP. If The conditional is true the value RAM[@SP-2] is changed to 0, else it is replaced with -1.
    #Also by adding the 'counterJmp' to the label name we ensure that the locations are unique
    elif command =='eq': 
        retStr='@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'D=M-D\n'+'@'+'JUMPTRUE'+counterJmp+'\n'+'D;'+'JEQ'+'\n'+'@SP\n'+'A=M-1\n'+'M=0\n'+'@'+'ENDJUMP'+counterJmp+'\n'+'0;JMP\n'+'(JUMPTRUE'+counterJmp+')\n'+'@SP\n'+'A=M-1\n'+'M=-1\n'+'(ENDJUMP'+counterJmp+')'
    elif command =='gt': 
        retStr='@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'D=M-D\n'+'@'+'JUMPTRUE'+counterJmp+'\n'+'D;'+'JGT'+'\n'+'@SP\n'+'A=M-1\n'+'M=0\n'+'@'+'ENDJUMP'+counterJmp+'\n'+'0;JMP\n'+'(JUMPTRUE'+counterJmp+')\n'+'@SP\n'+'A=M-1\n'+'M=-1\n'+'(ENDJUMP'+counterJmp+')'
    elif command =='lt': 
        retStr='@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'D=M-D\n'+'@'+'JUMPTRUE'+counterJmp+'\n'+'D;'+'JLT'+'\n'+'@SP\n'+'A=M-1\n'+'M=0\n'+'@'+'ENDJUMP'+counterJmp+'\n'+'0;JMP\n'+'(JUMPTRUE'+counterJmp+')\n'+'@SP\n'+'A=M-1\n'+'M=-1\n'+'(ENDJUMP'+counterJmp+')'
    
    return retStr

def generateMemoryAccess(command, segment, index):
    if command =="push": #Push opperation adds an element to the top of the stack.
        if segment =="constant":
            retStr = '@'+str(index)+'\n'+'D=A\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='local': #points at the base of current VM function's local segment. We save the value at @LCL+offset and then push it on the stack.
            retStr = '@LCL\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='argument': #We save the value at @ARG+offset and push it on the stack
            retStr = '@ARG\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='this': #Get the value at @THIS+offset and push it on top of the stack
            retStr = '@THIS\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='that': #Get the value at @THAT+offset and push it on top of the stack
            retStr = '@THAT\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='pointer': #pointer is mapped to locations 3-4 on RAM. Therefore 'push pointer i' is translated to assembly code that accesses RAM location 3+i.
            retStr = '@R3\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='temp': #temp is mapped to locations 5-12 on RAM. Therefore 'push temp i' is translated to assembly code that accesses RAM location 5+i.
            retStr = '@R5\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='static': #We represent each variable J in file F as a symbol F.J. We store the value at that address in D register and then push it on stack.
            retStr = '@'+str((sys.argv[1].split('.'))[0])+'.'+str(index)+'\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'

    elif command =="pop": #Pop opperation removes the top element from the stack.
        if segment =="local": # Store the value of the @LCL+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@LCL\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='argument': #Store the value of the @ARG+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@ARG\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='this': #Store the value of the @THIS+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@THIS\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='that': #Store the value of the @THAT+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@THAT\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='pointer': #Store the address of the desired offset in R13 register. Retrieve the value from top of the stack and put it inside the saved address location.
            retStr='@SP\n'+'M=M-1\n'+'@R3\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='temp':  #Store the address of the desired offset in R13 register. Retrieve the value from top of the stack and put it inside the saved address location.
            retStr='@SP\n'+'M=M-1\n'+'@R5\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='static': #Take the top element from the stack and put it inside the location of @F.J
            retStr = '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'@'+str((sys.argv[1].split('.'))[0])+'.'+str(index)+'\n'+'M=D'
    # Return a representation of Hack Assembly instruction(s) which implement the passed in command
    return retStr

def generateBranch(command, segment):
    if command == "label":
        retStr = f"label {segment}"
    elif command == "goto":
        retStr = f"@{segment}\n"+"0;JMP"
    elif command == "if-goto":
        retStr = "@SP\n"+"AM=M-1\n"+"D=M\n"+f"@{segment}\n"+"D;JNE"
    
    return retStr

def pushSegment(segment):
    instructions = [
        f'@{segment}',
        'D=M',
        '@SP',
        'M=M+1',
        'A=M-1',
        'M=D'
    ]
    return '\n'.join(instructions) 

def generateFunction(command, function, localVar):
    instructions = [f'({function})']    # Entry Label
    instructions += ['@SP','D=M','@LCL','M=D']
    for _ in range(int(localVar.strip())):
        instructions += ['@0','D=A','@SP','M=M+1','A=M-1','M=D']
    
    retStr = "\n".join(instructions)
    return retStr


def generateCall(command, function, args):
    global function_calls

    try:
        function_calls[function] += 1
        call_num = function_calls[function]
    except (KeyError):
        function_calls[function] = 0
        call_num = 0

    return_address = f'{function}$ret.{call_num}'
    instructions = [
        f'@{return_address}',
        'D=A',
        '@SP',
        'M=M+1',
        'A=M-1',
        'M=D',                      # push return address label to stack
        pushSegment('LCL'),
        pushSegment('ARG'),
        pushSegment('THIS'),
        pushSegment('THAT'),
        f'@{5 + int(args)}',             # number to subtract from SP to get to ARG
        'D=A',
        '@SP',
        'D=M-D',
        '@ARG',
        'M=D',                      # reposition ARG
        '@SP',
        'D=M',
        '@LCL',
        'M=D',                      # reposition LCL
        f'@{function}',
        '0;JMP',                    # call function (transfer control to callee)
        f'({return_address})'       # inject return address label into the code
    ]

    retStr = "\n".join(instructions)
    return retStr

def generateReturn(command):
    instructions = [
        '@LCL',
        'D=M',
        '@R13',
        'M=D',      # save LCL (end of frame) in temporary variable
        '@5',
        'A=D-A',
        'D=M',
        '@R14',
        'M=D',      # save return address in temporary variable
        '@SP',
        'A=M-1',
        'D=M',
        '@ARG',
        'A=M',
        'M=D',      # reposition return value for the caller
        'D=A+1',
        '@SP',
        'M=D',      # reposition stack pointer for the caller
        '@R13',
        'AM=M-1',
        'D=M',
        '@THAT',
        'M=D',      # restore THAT (that segment) for the caller
        '@R13',
        'AM=M-1',
        'D=M',
        '@THIS',
        'M=D',      # restore THIS (this segment) for the caller
        '@R13',
        'AM=M-1',
        'D=M',
        '@ARG',
        'M=D',      # restore ARG (argument segment) for the caller
        '@R13',
        'AM=M-1',
        'D=M',
        '@LCL',
        'M=D',      # restore LCL (local segment) for the caller
        '@R14',
        'A=M',
        '0;JMP'     # go to the return address
    ]

    retStr = "\n".join(instructions)
    return retStr
   
