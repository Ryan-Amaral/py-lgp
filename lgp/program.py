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

    def __init__(self, program=None, progSize=Program.maxProgSize, genCreate=0):
        if program is not None: # copy existing program (probably to be mutated)
            self.instructions = list(program.instructions)
        else: # create brand new program, all new instructions
            self.instructions = [random.randint(0,2**sum(Program.instLengths)-1)
                                 for _ in range(progSize)]

        # give a new id
        self.id = Program.idCount
        Program.idCount += 1

        self.genCreate = genCreate


    def run(input, regs, modes, ops, dsts, srcs, regSize):
        pass

    def getAction(self, obs):
        pass

    def mutate(self, pAdd=1, pDel=1, pSwp=1, pMut=1):
        pass

    def setInstructionBitLengths(lMode=Program.instLengths[0],
            lOp=Program.instLengths[1], lDest=Program.instLengths[2],
            lSrc=Program.instLengths[3]):
        Program.instLengths[0] = lMode
        Program.instLengths[1] = lOp
        Program.instLengths[2] = lDest
        Program.instLengths[3] = lSrc
