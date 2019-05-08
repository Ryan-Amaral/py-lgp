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
        changed = False # track if change was made

        # add instruction maybe
        if(len(self.instructions) < Program.maxProgSize and
                random.uniform(0,1) < pAdd):
            self.instructions.insert(
                random.randint(0, len(self.instructions)-1),
                random.randint(0,2**sum(Program.instLengths)-1))
                
            changed = True

        # delete instruction maybe
        if(len(self.instructions) > 1 and
                random.uniform(0,1) < pDel):
            del self.instructions[random.randint(0, len(self.instructions)-1)]

            changed = True

        # swap instructions maybe
        if random.uniform(0,1) < pSwp:
            idx1 = random.randint(0, len(self.instructions)-1)
            idx2 = random.randint(0, len(self.instructions)-1)
            while idx2 == idx1: # make sure different
                idx2 = random.randint(0, len(self.instructions)-1)

            tmp = self.instructions[idx1]
            self.instructions[idx1] = self.instructions[idx2]
            self.instructions[idx2] = tmp

            changed = True

        # mutate instruction maybe
        if random.uniform(0,1) < pMut:
            idx = random.randint(0, len(self.instructions)-1)
            inst = bin(self.instructions[idx]) # get binary rep
            # flip a random bit
            bit = random.randint(2, len(inst)-1)
            if inst[bit] == '0':
                self.instructions[idx] = int(inst[:bit] + '1' + inst[bit+1:])
            else:
                self.instructions[idx] = int(inst[:bit] + '0' + inst[bit+1:])

            changed = True

        return changed

    def setInstructionBitLengths(lMode=Program.instLengths[0],
            lOp=Program.instLengths[1], lDest=Program.instLengths[2],
            lSrc=Program.instLengths[3]):
        Program.instLengths[0] = lMode
        Program.instLengths[1] = lOp
        Program.instLengths[2] = lDest
        Program.instLengths[3] = lSrc
