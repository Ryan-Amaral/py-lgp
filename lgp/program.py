"""
A program which contains multiple instructions, each of which performing some
operation on some registers/inputs.
"""
class Program:
    maxProgSize = 128

    numOutRegs = 8 # registers that are mapped to outputs after running
    numMemRegs = 8 # registers that aren't cleared after a run
    numFgtRegs = 8 # registers that are cleared after each run

    idCount = 0 # unique numeric id of program, incremention on each new one

    def __init__(self, program=None, progSize=maxProgSize, genCreate=0):
        pass

    def run(input, regs, modes, ops, dsts, srcs, regSize):
        pass

    def getAction(obs):
        pass

    def mutate(self, pAdd=1, pDel=1, pSwp=1, pMut=1):
        pass
