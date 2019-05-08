import random

"""
A program which contains multiple instructions, each of which performing some
operation on some registers/inputs.
"""
class Program:
    maxProgSize = 128

    numOutRegs = 8 # registers that are mapped to outputs after running
    numMemRegs = 8 # registers that aren't cleared after a run
    numFgtRegs = 8 # registers that are cleared after each run

    idCount = 0 # unique numeric id of program, incrementing on each new one

    """
    bits for:
    mode   op    dest       src
    1      111   11111...   11111111111...

    Mode: Always 1 bit, whether to use register or input.
    Op: Always 3 bits, one of 8 math operations (add, sub, mult, div, cos, log,
        exp, neg).
    Dest: At-least # of bits to store # of registers. The register to place the
        result of the instruction into.
    Src: At-least # of bits to store size of input. The index to take from
        input, or a register depending on Mode.
    """
    instLengths = [1,3,5,23]

    def __init__(self, program=None, progSize=maxProgSize, genCreate=0):
        if program is not None:
            self.instructions = list(program.instructions)
        else:
            instSize = 1+
            self.instructions = [random.randint(0,5) for _ in range(10)]

    def run(input, regs, modes, ops, dsts, srcs, regSize):
        pass

    def getAction(self, obs):
        pass

    def mutate(self, pAdd=1, pDel=1, pSwp=1, pMut=1):
        pass

    def setInstructionBitLengths(lMode=instLengths[0], lOp=instLengths[1],
            lDest=instLengths[2], lSrc=instLengths[3]):
        instLengths[0] = lMode
        instLengths[1] = lOp
        instLengths[2] = lDest
        instLengths[3] = lSrc
