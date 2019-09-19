import random
from lgp.program import Program

"""
A team is a collection of programs that work together to produce multiple
actions at each step.
"""
class Team:

    idCount = 0

    def __init__(self, team=None, teamSize=1, genCreate=0):
        self.programs = []
        self.genCreate = genCreate
        self.outcomes = {} # stores rewards for tasks
        # give a new id
        self.id = Team.idCount
        Team.idCount += 1

        if team is not None: # clone team
            for prog in team.programs:
                self.programs.append(prog)
        else: # create new team (generate programs)
            self.programs = [Program(progSize=random.randint(1,Program.maxProgSize),
                                     genCreate=genCreate)
                                for _ in range(teamSize)]

        # track references, +1 for clone, =1 for new
        for prog in self.programs:
            try:
                prog.refs += 1
            except:
                prog.refs = 1

    """
    Gets the action from each program in team (0th register).
    """
    def getAction(self, obs):
        return [prog.getAction(obs)[0] for prog in self.programs]

    def mutate(self, pDel, pSwp, pMut, allPrograms, gen,
                    pAddInst, pDelInst, pSwpInst, pMutInst):

        changed = False
        while not changed:
            # first delete any programs
            p = pDel
            redo = False
            while random.uniform(0,1) < pDel or redo:
                p *= pDel
                idx = random.randint(0,len(self.programs)-1)
                try:
                    redo = False
                    self.programs[idx].refs -= 1
                    self.programs[idx] = None
                    changed = True
                except:
                    redo = True
                    p /= pDel

            # then add in to fill up deleted
            for i in range(len(self.programs)):
                if self.programs[i] is None:
                    self.programs[i] = random.choice(allPrograms)
                    self.programs[i].refs += 1

            # then swap any
            p = pSwp
            while random.uniform(0,1) < pSwp:
                p *= pSwp
                idx1, idx2 = random.sample(range(len(self.programs)), 2)
                tmp = self.programs[idx1]
                self.programs[idx1] = self.programs[idx2]
                self.programs[idx2] = tmp
                changed = True

            # then mutate any
            p = pMut
            while random.uniform(0,1) < pMut:
                p *= pMut
                idx = random.randint(0,len(self.programs)-1)
                self.programs[idx].refs -= 1
                self.programs[idx] = Program(program=self.programs[idx], genCreate=gen)
                self.programs[idx].mutate(pAddInst, pDelInst, pSwpInst, pMutInst)
                self.programs[idx].refs = 1
                changed = True


    def reward(self, task, score):
        self.outcomes[task] = score
