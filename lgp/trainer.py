import random

"""
Creates and maintains a population of programs.
"""
class Trainer:

    def __init__(self, popSize=200, gap=0.5, maxProgSize=128,
            numOutRegs=8, numMemRegs=16, numFgtRegs=8,
            pInstAdd=1, pInstDel=1, pInstSwp=1, pInstMut=1, pProgMut=1):

        self.popSize = popSize
        self.initPop()

    def initPop(self):
        self.programs = [Program(progSize=random.randint(1,self.maxProgSize))
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
                        key=lambda prg: prg.outcomes.get(tasks, None))
            else: # multi task
                pass # implement later when needed

    def evolve(self):
        pass

    def select(self):
        pass

    def generate(self):
        pass
