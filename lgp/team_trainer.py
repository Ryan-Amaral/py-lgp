import random
from lgp.program import Program
from lgp.team import Team

"""
Creates and maintains a population of programs.
"""
class TeamTrainer:

    def __init__(self, numActions, popSize=200, gap=0.5, maxProgSize=128,
            numOutRegs=8, numMemRegs=0, numFgtRegs=0,
            pProgDel=0.7, pProgSwp=0.6, pProgMut=0.65,
            pInstAdd=0.08, pInstDel=0.06, pInstSwp=0.05, pInstMut=0.05):

        self.numActions = numActions

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

        self.pProgDel=pProgDel
        self.pProgSwp = pProgSwp
        self.pProgMut = pProgMut

        self.curGen = 0

        self.initPop()

        self.scoreStats = {}

    def initPop(self):
        # create teams (each creating its programs)
        self.teams = [Team(teamSize=self.numActions, genCreate=self.curGen)
                        for _ in range(self.popSize)]

        # track all created programs too
        self.programs = []
        for team in self.teams:
            for program in team.programs:
                self.programs.append(program)

    """
    Returns all of the agents/programs. Sorted arbitrarilly unless sortTasks are
    specified (single or list). Type is how to deal with multiple tasks ('min',
    'max','avg','sum','paretoDominate','paretoNonDominated'). norm is whether to
    normalize scores, good for pretty much all multiTask. skipTasks determine
    individuals to skip if all tasks have scores. If byFitness, then uses just
    stored fitness on agents.
    """
    def getAgents(self, sortTasks=[], scoreType='min', norm=True, skipTasks=[]):
        teams = [team for team in self.teams
                    if len(skipTasks) == 0
                        or any(task not in team.outcomes for task in skipTasks)]

        if len(sortTasks) == 0:
            return list(teams)
        else:
            return sorted(teams, key=lambda t: t.outcomes[sortTasks[0]], reverse=True)

    def applyScores(self, scores): # used when multiprocessing
        for score in scores:
            for team in self.teams:
                if score[0] == team.id:
                    for task, outcome in score[1].items():
                        team.outcomes[task] = outcome
                    break # on to next score

        return self.teams

    def evolve(self, tasks, fitType='min'):
        self.getScoreStats(tasks)
        self.select(tasks, fitType)
        self.generate()
        self.curGen += 1

        # track new programs
        for team in self.teams:
            for prog in team.programs:
                if prog not in self.programs:
                    self.programs.append(prog)

        for program in self.programs:
            program.clearRegisters()

    def select(self, tasks, fitType, norm=True): # select programs to keep
        numKeep = self.popSize - int(self.popSize * self.gap) # # agents to keep
        rankedTeams = sorted(self.teams, key=lambda t: t.outcomes[tasks[0]], reverse=True)
        self.teams = rankedTeams[:numKeep]
        delTeams = rankedTeams[numKeep:]

        for team in delTeams:
            for prog in team.programs:
                prog.refs -= 1
                if prog.refs == 0: # no more references (remove prog)
                    self.programs.remove(prog)

    def generate(self): # generate new programs
        parents = list(self.teams)
        # generate this many new ones
        for i in range((self.popSize - len(self.teams))):
            p = random.choice(parents)
            newTeam = Team(team=p, genCreate=self.curGen)
            newTeam.mutate(pDel=self.pProgDel, pSwp=self.pProgSwp, pMut=self.pProgMut,
                            allPrograms=list(self.programs), gen=self.curGen,
                            pAddInst=Program.pInstAdd, pDelInst=Program.pInstDel,
                                pSwpInst=Program.pInstSwp, pMutInst=Program.pInstMut)
            self.teams.append(newTeam)

    def getScoreStats(self, tasks):
        if not isinstance(tasks, str):
            tasks = tasks[0] # deal with multi task reporting later
        scores = []
        for team in self.teams:
            scores.append(team.outcomes.get(tasks, None))

        self.scoreStats = {}
        self.scoreStats['scores'] = scores
        self.scoreStats['min'] = min(scores)
        self.scoreStats['max'] = max(scores)
        self.scoreStats['average'] = sum(scores)/len(scores)

        return self.scoreStats
