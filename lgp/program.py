import random
import numpy as np
from numba import njit
import math

"""
A program which contains multiple instructions, each of which performing some
operation on some registers/inputs.
"""
class Program:
    maxProgSize = 128

    numOutRegs = 8 # registers that are mapped to outputs after running
    numMemRegs = 8 # registers that aren't cleared after a run
    numFgtRegs = 8 # registers that are cleared after each run

    # probabilities for various program mutations
    pInstAdd = 1
    pInstDel = 1
    pInstSwp = 1
    pInstMut = 1

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

    def __init__(self, program=None, progSize=-1, genCreate=0):
        if progSize == -1:
            progSize = Program.maxProgSize

        if program is not None: # copy existing program (probably to be mutated)
            self.instructions = list(program.instructions)
        else: # create brand new program, all new instructions
            Program.maxInst = 2**sum(Program.instLengths)-1
            self.instructions = [random.randint(0,Program.maxInst)
                                 for _ in range(progSize)]

        # give a new id
        self.id = Program.idCount
        Program.idCount += 1

        self.genCreate = genCreate

        # initialize registers
        self.registers = np.zeros(Program.numOutRegs+Program.numMemRegs+
                Program.numFgtRegs)

        # store instructions in a way for fast execution
        self.extractInstructionsData()

        self.outcomes = {} # stores rewards for tasks

        self.fitness = None

    """
    Produces an action based on the observation and state of registers.
    actionType 'single' returns the index of the max output register, 'multi'
    returns all output registers.
    """
    def getAction(self, obs, actionType='multi'):
        # reset fgt registers
        self.clearRegisters(clearAll=False)

        Program.run(obs, self.registers,
                self.modes, self.ops, self.dests, self.srcs)

        if actionType == 'multi':
            return self.registers[:Program.numOutRegs]
        else:
            return np.argmax(self.registers[:Program.numOutRegs])

    def clearRegisters(self, clearAll=True):
        if clearAll:
            self.registers = np.zeros(Program.numOutRegs+Program.numMemRegs+
                    Program.numFgtRegs)
        else:
            # reset fgt registers
            for i in range(Program.numFgtRegs):
                self.registers[Program.numOutRegs+Program.numMemRegs+i] = 0

    def mutate(self, pAdd=-1, pDel=-1, pSwp=-1, pMut=-1):
        if pAdd == -1:
            pAdd = Program.pInstAdd
        if pDel == -1:
            pDel = Program.pInstDel
        if pSwp == -1:
            pSwp = Program.pInstSwp
        if pMut == -1:
            pMut = Program.pInstMut

        changed = False # track if change was made

        oLen = len(self.instructions) # to give all operators equal chances

        # Deleting
        for i in range(oLen):
            # delete instruction maybe
            if(len(self.instructions) > 1 and
                    random.uniform(0,1) < pDel):
                del self.instructions[random.randint(0, len(self.instructions)-1)]

                changed = True

        # Swapping
        for i in range(oLen):
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

        # Mutating
        for i in range(oLen):
            # mutate instruction maybe
            if random.uniform(0,1) < pMut:
                idx = random.randint(0, len(self.instructions)-1)
                inst = bin(self.instructions[idx]) # get binary rep
                # flip a random bit
                bit = random.randint(2, len(inst)-1) # start at 2 for '0b' prefix
                if inst[bit] == '0':
                    self.instructions[idx] = int(inst[:bit] + '1' + inst[bit+1:], 2)
                else:
                    self.instructions[idx] = int(inst[:bit] + '0' + inst[bit+1:], 2)

                changed = True

        # Adding
        for i in range(oLen):
            # add random instruction maybe
            if(len(self.instructions) < Program.maxProgSize and
                    random.uniform(0,1) < pAdd):
                self.instructions.insert(
                    random.randint(0, len(self.instructions)-1),
                    random.randint(0,2**sum(Program.instLengths)-1))

                changed = True

        # update data
        self.extractInstructionsData()

        return changed

    def reward(self, task, score):
        self.outcomes[task] = score

    """
    Gets the score(s) of the program based on provided tasks. Types: 'min', 'max',
    'avg', 'sum', 'pareto'. minMaxs is a list the size of tasks in 2-tuples being
    <min,max> of all program scores for each task.
    """
    def getScore(self, tasks, sType='min', minMaxs=None):
        # just return single value
        if len(tasks) == 1:
            return self.outcomes[tasks[0]]

        outcomes = [self.outcomes[task] for task in tasks]

        # normalize
        if minMaxs is not None:
            for i,mm in enumerate(minMaxs):
                try:
                    outcomes[i] = (outcomes[i]-mm[0])/(mm[1]-mm[0])
                except:
                    outcomes[i] = 0

        # return value as specified
        if sType == 'min':
            return min(outcomes)
        elif sType == 'max':
            return max(outcomes)
        elif sType == 'avg':
            return sum(outcomes)/len(outcomes)
        elif sType == 'sum':
            return sum(outcomes)
        elif 'pareto' in sType:
            return outcomes

    """
    Get min and max scores among population for each task.
    """
    def getOverallMinMaxs(tasks, progs):
        if isinstance(tasks, str):
            tasks = [tasks]
        # initial min maxs from fist individual
        minMaxs = [[progs[0].outcomes[tsk], progs[0].outcomes[tsk]]
                    for tsk in tasks]

        # update mins and maxs with program outcomes
        for prog in progs[1:]:
            for i, task in enumerate(tasks):
                cur = prog.outcomes[task]
                if cur < minMaxs[i][0]:
                    minMaxs[i][0] = cur
                elif cur > minMaxs[i][1]:
                    minMaxs[i][1] = cur

        return minMaxs

    def extractInstructionsData(self): # for efficiency in running
        instsData = np.array([
            [
                Program.getIntSegment(inst, 0, Program.instLengths[0]),
                Program.getIntSegment(inst, Program.instLengths[0],
                        Program.instLengths[1]),
                Program.getIntSegment(inst, sum(Program.instLengths[:2]),
                        Program.instLengths[2]),
                Program.getIntSegment(inst, sum(Program.instLengths[:3]),
                        Program.instLengths[3])
            ]
            for inst in self.instructions])

        self.modes = np.array(instsData[:,0], dtype = bool)
        self.ops = np.array(instsData[:,1], dtype = np.int8)
        self.dests = np.array(instsData[:,2], dtype = np.int8)
        self.srcs = np.array(instsData[:,3], dtype = np.int32)

    def setInstructionBitLengths(lMode=-1, lOp=-1, lDest=-1, lSrc=-1):
        if lMode == -1:
            lMode = Program.instLengths[0]
        if lOp == -1:
            lOp = Program.instLengths[1]
        if lDest == -1:
            lDest = Program.instLengths[2]
        if lSrc == -1:
            lSrc = Program.instLengths[3]

        Program.instLengths[0] = lMode
        Program.instLengths[1] = lOp
        Program.instLengths[2] = lDest
        Program.instLengths[3] = lSrc

    def getIntSegment(num, bitStart, bitLen):
        binStr = format(num, 'b').zfill(sum(Program.instLengths))
        return int(binStr[bitStart:bitStart+bitLen], 2)

    @njit
    def run(inpt, regs, modes, ops, dsts, srcs):
        regSize = len(regs)
        inptLen = len(inpt)
        for i in range(len(modes)):
            # first get source
            if modes[i] == False:
                src = regs[srcs[i]%regSize]
            else:
                src = inpt[srcs[i]%inptLen]

            # do operation
            op = ops[i]
            x = regs[dsts[i]]
            y = src
            dest = dsts[i]%regSize
            if op == 0:
                regs[dest] = x+y
            elif op == 1:
                regs[dest] = x-y
            elif op == 2:
                regs[dest] = x*y
            elif op == 3:
                if y != 0:
                    regs[dest] = x/y
            elif op == 4:
                regs[dest] = math.cos(y)
            elif op == 5:
                if y > 0:
                    regs[dest] = math.log(y)
            elif op == 6:
                regs[dest] = math.exp(y)
            elif op == 7:
                if x < y:
                    regs[dest] = x*(-1)

            if math.isnan(regs[dest]):
                regs[dest] = 0
            elif regs[dest] == np.inf:
                regs[dest] = np.finfo(np.float64).max
            elif regs[dest] == np.NINF:
                regs[dest] = np.finfo(np.float64).min
