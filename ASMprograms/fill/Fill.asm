// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// Pseudo Code
// kb = 24576
// LOOP:
//     sc = 16384
//     Check M @24576
//     if M>0: goto BLACK
//     else: goto WHITE
// BLACK:
//     while 24575-sc > 0:
//         @sc M = -1
//         sc += 1
//     goto LOOP
// WHITE:
//     while 24575-sc > 0:
//         @sc M = 0
//         sc += 1
//     goto LOOP


@24576
D=A 
@kb 
M=D

(LOOP)
@16384
D=A 
@sc 
M=D

@24576
D=M 
@BLACK
D; JGT
@WHITE
D; JEQ

(BLACK)
@sc
A=M 
M=-1
@24575
D=A 
@sc
D=D-M 
M=M+1
@BLACK
D; JGT
@LOOP
D; JEQ

(WHITE)
@sc
A=M 
M=0
@24575
D=A 
@sc
D=D-M 
M=M+1
@WHITE
D; JGT
@LOOP
D; JEQ