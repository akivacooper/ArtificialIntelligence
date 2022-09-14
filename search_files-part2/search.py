#search

import state
import frontier

def search(n):
    new_state = state.create(n)
    # print(new_state)
    new_frontier = frontier.create(new_state)
    while not frontier.is_empty(new_frontier):
        new_state = frontier.remove(new_frontier)
        if state.is_target(new_state):
            return [new_state, new_frontier[1], new_frontier[2]]
        next_state=state.get_next(new_state)
        for i in next_state:
            frontier.insert(new_frontier,i)
    return 0


totalPushes = 0
totalPops = 0
totalLength = 0

for x in range(100):
    answer = search(4)
    totalPushes += answer[1]
    totalPops += answer[2]
    totalLength += len(answer[0][1])

averagePushes = totalPushes/100
averagePops = totalPops/100
averageLength = totalLength/100

print("Average pushes: ", averagePushes)
print("Average pops: ", averagePops)
print("Average length: ", averageLength)





