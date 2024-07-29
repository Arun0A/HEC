def parser(inst):
    items = (inst.strip()).split(" ")
    command = items[0]
    
    if len(items)==1: 
        tup = ('C_ARITHMETIC',(command,None))
        if command == "return":
            tup = ("C_RETURN",(command))

    elif command.strip()=="push": 
        tup = ('C_PUSH',(command,(items[1],items[2])))
    elif command.strip()=="pop": 
        tup = ('C_POP',(command,(items[1],items[2])))

    elif command.strip() in ['label', 'goto', 'if-goto']:
        tup = ('C_BRANCH',(command,items[1])) # parseBranch(lineArr)

    elif command.strip()=="function":
        tup = ("C_FUNCTION",(command, (items[1], items[2])))
    elif command.strip()=="call":
        tup = ("C_CALL",(command, (items[1], items[2])))

    return tup