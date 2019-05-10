import random
from program import Program

"""
Creates and maintains a population of programs.
"""
class Trainer:

    def __init__(self, numActions, popSize=200, gap=0.5, maxProgSize=128,
            numMemRegs=16, numFgtRegs=8,
            pInstAdd=1, pInstDel=1, pInstSwp=1, pInstMut=1, pProgMut=1):

        self.popSize = popSize
        self.gap = gap

        Program.maxProgSize = maxProgSize
        Program.numOutRegs = numActions
        Program.numMemRegs = numMemRegs
        Program.numFgtRegs = numFgtRegs
        Program.pInstAdd = pInstAdd
        Program.pInstDel = pInstDel
        Program.pInstSwp = pInstSwp
        Program.pInstMut = pInstMut

        self.curGen = 0

        self.initPop()

    def initPop(self):
        self.programs = [Program(progSize=random.randint(1,self.maxProgSize),
                                 getCreate=self.curGen)
                        for _ in range(self.popSize)]

    """
    Returns all of the agents/programs. Sorted arbitrarilly unless tasks are
    specified (single or list). Type is how to deal with multiple tasks ('min',
    'avg').
    """
    def getAgents(self, tasks=None, type='min'):
        if tasks is None: # just return all programs
            return list(self.programs)
        else: # sort based on fitnesses
            if isinstance(tasks, str): # single task
                return sorted(self.programs,
                        key=lambda prg: prg.outcomes.get(tasks, None),
                        reverse=True)
            else: # multi task
                pass # implement later when needed

    def evolve(self, tasks, fitType='min'):
        self.select(tasks, fitType)
        self.generate()
        self.curGen += 1

    def select(self, tasks, fitType):
        numKeep = self.popSize - int(self.popSize * self.gap) # agents to keep
        if isinstance(tasks, str): # single task
            self.programs = sorted(self.programs,
                    key=lambda prg: prg.outcomes.get(tasks, None),
                    reverse=True)[:numKeep]
        else: # multi task
            pass

    def generate(self):
        # generate this many new ones
        for i in range(self.popSize - len(self.programs)):
            # for now just create randoms for testing
            self.programs.append(
                    Program(progSize=random.randint(1,self.maxProgSize),
                            getCreate=self.curGen))