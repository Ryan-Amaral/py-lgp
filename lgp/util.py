from operator import itemgetter

"""
Takes in agents and scores, and returns the agents sorted descending based on
pareto points.
"""
def pareto1(agents, scores, reverse=True):
    agentPoints = []
    for i in range(len(agents)):
        ap = 0
        for j in range(len(agents)):
            if i == j:
                continue # don't compare to self
            if all([scores[i][k] >= scores[j][k]
                     for k in range(len(scores[i]))])]):
                ap += 1
        agentPoints.append((agents[i], ap))

    agentPoints.sort(key=itemgetter(1), reverse=reverse)

    return [ap[0] for ap in agentPoints]
