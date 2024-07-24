def parser(inst):
    items = (inst.strip()).split(" ")
    command = items[0]
    
    if len(items)==1: 
        tup = ('C_ARITHMETIC',(command,None))

    elif len(items)==3: 
        if command =="push": 
            tup = ('C_PUSH',(command,(items[1],items[2])))
        else: 
            tup = ('C_POP',(command,(items[1],items[2])))
    
    return tup