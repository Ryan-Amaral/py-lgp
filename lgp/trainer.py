import random
from lgp.program import Program

"""
Creates and maintains a population of programs.
"""
class Trainer:

    def __init__(self, numActions, popSize=200, gap=0.5, maxProgSize=128,
            numMemRegs=8, numFgtRegs=8,
            pInstAdd=0.2, pInstDel=0.2, pInstSwp=0.2, pInstMut=0.2, pProgMut=1):

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
        self.programs = [Program(progSize=random.randint(1,Program.maxProgSize),
                                 genCreate=self.curGen)
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

    def applyScores(self, scores): # used when multiprocessing
        for score in scores:
            for program in self.programs:
                if score[0] == program.id:
                    for task, outcome in score[1].items():
                        program.outcomes[task] = outcome
                    break # on to next score

        return self.programs

    def evolve(self, tasks, fitType='min'):
        self.select(tasks, fitType)
        self.generate()
        self.curGen += 1
        for program in self.programs:
            program.clearRegisters()

    def select(self, tasks, fitType): # select programs to keep
        numKeep = self.popSize - int(self.popSize * self.gap) # agents to keep
        if isinstance(tasks, str): # single task
            self.programs = sorted(self.programs,
                    key=lambda prg: prg.outcomes.get(tasks, None),
                    reverse=True)[:numKeep]
        else: # multi task
            pass

    def generate(self): # generate new programs
        parents = list(self.programs)
        # generate this many new ones
        for i in range(int((self.popSize - len(self.programs))/2)):
            p1,p2 = random.sample(parents, 2)
            # crossover point
            crsPt = random.randint(0,
                    min(len(p1.instructions), len(p2.instructions))-1)

            newProg1 = Program(genCreate=self.curGen)
            newProg2 = Program(genCreate=self.curGen)

            newProg1.instructions = (p1.instructions[:crsPt] +
                                    p2.instructions[crsPt:])
            newProg2.instructions = (p2.instructions[:crsPt] +
                                    p1.instructions[crsPt:])

            newProg1.mutate()
            newProg2.mutate()

            self.programs.append(newProg1)
            self.programs.append(newProg2)
