# py-lgp

## Installation
Clone this repo, then `pip install .` in the repo's root directory (where this README is).

## Minimal Usage Example
```python
from lgp.trainer import Trainer
from lgp.program import Program

# Manager of the population of programs
trainer = Trainer(numActions=10)

while True:
  # list of agents/programs
  agents = trainer.getAgents(skipTasks=[options.envName])

  """
  Put code for running all agents here. Dependant on environment.
  https://github.com/Ryan-Amaral/roboschool-ga/blob/master/run-lgp.py for an example.
  """

  trainer.evolve(tasks=options.envName)
  
  # some other usefull bits
  scoreStats = trainer.scoreStats # for summary of scores that generation
  bestProg = trainer.getAgents(sortTasks=taskName)[0] # to get top scoring program
```

