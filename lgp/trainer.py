import random
from lgp.program import Program

"""
Creates and maintains a population of programs.
"""
class Trainer:

    def __init__(self, numActions, popSize=200, gap=0.5, maxProgSize=128,
            numMemRegs=8, numFgtRegs=8,
            pInstAdd=0.08, pInstDel=0.06, pInstSwp=0.05, pInstMut=0.05, pProgMut=1):

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

        self.scoreStats = {}

    def initPop(self):
        self.programs = [Program(progSize=random.randint(1,Program.maxProgSize),
                                 genCreate=self.curGen)
                        for _ in range(self.popSize)]

    """
    Returns all of the agents/programs. Sorted arbitrarilly unless sortTasks are
    specified (single or list). Type is how to deal with multiple tasks ('min',
    'avg'). skipTasks determine individuals to skip if all tasks have scores.
    """
    def getAgents(self, sortTasks=None, type='min', skipTasks=[]):
        if sortTasks is None: # just return all programs
            return list(self.programs)
        else: # sort based on fitnesses
            if isinstance(sortTasks, str): # single task
                return [prog for prog in sorted(self.programs,
                        key=lambda prg: prg.outcomes.get(sortTasks, None),
                        reverse=True) if any(task not in prog.outcomes for task
                        in skipTasks)]
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
        self.getScoreStats(tasks)
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
        for i in range((self.popSize - len(self.programs))):
            p = random.choice(parents)
            newProg = Program(genCreate=self.curGen)
            newProg.instructions = list(p.instructions)
            newProg.mutate()
            self.programs.append(newProg)

    def getScoreStats(self, tasks):
        scores = []
        for prog in self.programs:
            scores.append(prog.outcomes.get(tasks, None))

        self.scoreStats = {}
        self.scoreStats['scores'] = scores
        self.scoreStats['min'] = min(scores)
        self.scoreStats['max'] = max(scores)
        self.scoreStats['average'] = sum(scores)/len(scores)

        return self.scoreStats
