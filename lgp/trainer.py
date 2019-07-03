import random
from lgp.program import Program
from lgp.util import pareto1

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
    'max','avg','sum','pareto'). norm is whether to normalize scores, good for
    pretty much all multiTask. skipTasks determine individuals to skip if all
    tasks have scores. If byFitness, then uses just stored fitness on agents.
    """
    def getAgents(self, sortTasks=None, scoreType='min', norm=True, skipTasks=[]):
        if sortTasks is None: # just return all programs
            return list(self.programs)
        else: # return sorted by new ranking
            return [prog for prog in self.progsScorer(sortTasks, scoreType, norm)
                    if any(task not in prog.outcomes for task in skipTasks)
                        or len(skipTasks) == 0]

    """
    Wrapper around getting scores from program, for all programs, to clean up
    calls from mess from pareto, getting minMaxs, etc. Sorted. If saveFitness,
    stores the score in fitness variable of program.
    """
    def progsScorer(self, tasks, scoreType, norm, reverse=True):
        # get min and max of each task for normalizing
        minMaxs = None
        if norm:
            minMaxs = Program.getOverallMinMaxs(tasks, self.programs)

        if scoreType != 'pareto': # just return obtained score
            return sorted(self.programs,
                    key=lambda prg:
                           prg.getScore(tasks, sType=scoreType, minMaxs=minMaxs),
                    reverse=reverse)
        else: # score based pareto front type stuff
            return pareto1(self.programs,
                            [prg.getScore(tasks, sType=scoreType, minMaxs=minMaxs)
                                for prg in self.programs], reverse=reverse)


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

    def select(self, tasks, fitType, norm=True): # select programs to keep
        numKeep = self.popSize - int(self.popSize * self.gap) # # agents to keep
        self.programs = self.progsScorer(tasks, fitType, norm)[:numKeep]

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
        if not isinstance(tasks, str):
            tasks = tasks[0] # deal with multi task reporting later
        scores = []
        for prog in self.programs:
            scores.append(prog.outcomes.get(tasks, None))

        self.scoreStats = {}
        self.scoreStats['scores'] = scores
        self.scoreStats['min'] = min(scores)
        self.scoreStats['max'] = max(scores)
        self.scoreStats['average'] = sum(scores)/len(scores)

        return self.scoreStats
