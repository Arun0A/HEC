// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// TO PERFORM R2 = R0*R1

// Pseudo Code
// ===========
// n = R1
// i = 1
// mul = 0

// LOOP:
// if i>n goto STOP
// mul = mul + R0
// i = i+1
// goto LOOP

// STOP:
// R2 = mul

@R1
D=M 
@n
M=D

@i
M=1

@mul
M=0

@R2
M=0

(LOOP)
@i
D=M
@n
D=D-M
@STOP 
D;JGT

@R0
D=M 
@mul
M=D+M 

@i 
M=M+1

@LOOP
0;JMP

(STOP)
@mul
D=M 
@R2
M=D

(END)
@END
0;JMP
