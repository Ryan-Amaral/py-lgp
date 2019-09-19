from operator import itemgetter
import pickle
#from lgp.trainer import Trainer
from lgp.program import Program
from lgp.team import Team

"""
Rank agents based on how many other agents they dominate.
"""
def paretoDominate(agents, scores, reverse=True):
    agentPoints = []
    for i in range(len(agents)):
        ap = 0
        for j in range(len(agents)):
            if i == j:
                continue # don't compare to self
            if all([scores[i][k] >= scores[j][k]
                     for k in range(len(scores[i]))]):
                ap += 1
        agentPoints.append((agents[i], ap))

    agentPoints.sort(key=itemgetter(1), reverse=reverse)

    return [ap[0] for ap in agentPoints]

"""
Rank agents based on how many other agents don't dominate it
"""
def paretoNonDominated(agents, scores, reverse=True):
    agentPoints = []
    for i in range(len(agents)):
        ap = 0
        for j in range(len(agents)):
            if i == j:
                continue # don't compare to self
            if all([scores[i][k] < scores[j][k]
                     for k in range(len(scores[i]))]):
                ap -= 1
        agentPoints.append((agents[i], ap))

    agentPoints.sort(key=itemgetter(1), reverse=reverse)

    return [ap[0] for ap in agentPoints]

def saveProgram(fileName, program):
    # save class variables to program instance, to be loaded back.
    program.maxProgSize = Program.maxProgSize
    program.numOutRegs = Program.numOutRegs
    program.numMemRegs = Program.numMemRegs
    program.numFgtRegs = Program.numFgtRegs
    program.pInstAdd = Program.pInstAdd
    program.pInstDel = Program.pInstDel
    program.pInstSwp = Program.pInstSwp
    program.pInstMut = Program.pInstMut
    program.idCount = Program.idCount
    program.instLengths = list(Program.instLengths)

    pickle.dump(program, open(fileName, 'wb'))

def loadProgram(fileName):
    program = pickle.load(open(fileName, 'rb'))

    # load class variables back
    Program.maxProgSize = program.maxProgSize
    Program.numOutRegs = program.numOutRegs
    Program.numMemRegs = program.numMemRegs
    Program.numFgtRegs = program.numFgtRegs
    Program.pInstAdd = program.pInstAdd
    Program.pInstDel = program.pInstDel
    Program.pInstSwp = program.pInstSwp
    Program.pInstMut = program.pInstMut
    Program.idCount = program.idCount
    Program.instLengths = list(program.instLengths)

    return program

def saveTrainer(fileName, trainer):
    # save class variables to program instance, to be loaded back.
    trainer.maxProgSize = Program.maxProgSize
    trainer.numOutRegs = Program.numOutRegs
    trainer.numMemRegs = Program.numMemRegs
    trainer.numFgtRegs = Program.numFgtRegs
    trainer.pInstAdd = Program.pInstAdd
    trainer.pInstDel = Program.pInstDel
    trainer.pInstSwp = Program.pInstSwp
    trainer.pInstMut = Program.pInstMut
    trainer.idCount = Program.idCount
    trainer.instLengths = list(Program.instLengths)

    pickle.dump(trainer, open(fileName, 'wb'))

def loadTrainer(fileName):
    trainer = pickle.load(open(fileName, 'rb'))

    # load class variables back
    Program.maxProgSize = trainer.maxProgSize
    Program.numOutRegs = trainer.numOutRegs
    Program.numMemRegs = trainer.numMemRegs
    Program.numFgtRegs = trainer.numFgtRegs
    Program.pInstAdd = trainer.pInstAdd
    Program.pInstDel = trainer.pInstDel
    Program.pInstSwp = trainer.pInstSwp
    Program.pInstMut = trainer.pInstMut
    Program.idCount = trainer.idCount
    Program.instLengths = list(trainer.instLengths)

    return trainer

def saveTeam(fileName, team):
    # save class variables to program instance, to be loaded back.
    team.ProgmaxProgSize = Program.maxProgSize
    team.numOutRegs = Program.numOutRegs
    team.numMemRegs = Program.numMemRegs
    team.numFgtRegs = Program.numFgtRegs
    team.pInstAdd = Program.pInstAdd
    team.pInstDel = Program.pInstDel
    team.pInstSwp = Program.pInstSwp
    team.pInstMut = Program.pInstMut
    team.idCount = Program.idCount
    team.instLengths = list(Program.instLengths)
    team.tIdCount = Team.idCount

    pickle.dump(team, open(fileName, 'wb'))

def loadTeam(fileName):
    team = pickle.load(open(fileName, 'rb'))

    # load class variables back
    Program.maxProgSize = team.maxProgSize
    Program.numOutRegs = team.numOutRegs
    Program.numMemRegs = team.numMemRegs
    Program.numFgtRegs = team.numFgtRegs
    Program.pInstAdd = team.pInstAdd
    Program.pInstDel = team.pInstDel
    Program.pInstSwp = team.pInstSwp
    Program.pInstMut = team.pInstMut
    Program.idCount = team.idCount
    Program.instLengths = list(team.instLengths)
    Team.idCount = team.tIdCount

    return team

# implement teamTrainer load/save
