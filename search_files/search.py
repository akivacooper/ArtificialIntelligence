# search

import state
import frontier


def search(boardWidth):
    newState = state.create(boardWidth)
    #print(newState)
    newFrontier = frontier.create(newState)
    while not frontier.is_empty(newFrontier):
        newState = frontier.remove(newFrontier)
        if state.is_target(newState):
            return [newState, newFrontier[1], newFrontier[4], newFrontier[5]]
        nextState = state.get_next(newState)
        # print(nextState)
        for i in nextState:
            frontier.insert(newFrontier, i)
    return 0


totalDepth = 0
totalPushed = 0
totalPopped = 0

for x in range(100):
    print(x)
    answer = search(4)
    totalDepth += answer[1]
    totalPushed += answer[2]
    totalPopped += answer[3]

averageDepth = totalDepth / 100
averagePushes = totalPushed / 100
averagePopped = totalPopped / 100
print("Average depth: ", averageDepth)
print("Average number pushed: ", averagePushes)
print("Average number popped: ", averagePopped)
