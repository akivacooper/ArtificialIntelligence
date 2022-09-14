import stack
import state

#[stack, max. depth, init. state, try next level?,
# , total items pushed] The last one needs to be added
def create(initialState):
    newStack=stack.create(initialState)
    return [newStack, 1, initialState, False, 0, 0]

def is_empty(s):
    return stack.is_empty(s[0]) and not s[3] # stack is empty and try next level is false

def insert(frontier, x):
    frontier[4] = frontier[4] + 1
    if state.path_len(x)<=frontier[1]: # check if x is not too deep
        stack.insert(frontier[0], x)    # insert x to stack
    else:
        frontier[3]=True               # there is a reason to search deeper if needed
    
def remove(frontier):
    frontier[5] = frontier[5] + 1
    if stack.is_empty(frontier[0]):    # check is there are no states in the stack
        if frontier[3]:                # check if there is a reason to search deeper
            frontier[1]+=1             # increase search depth
            frontier[3]=False          # meanwhile there is no evidence to need to search deeper
            #print(s[1])         # print what level we finished searching
            return frontier[2]         # return the initial state
        else:
            return 0
    return stack.remove(frontier[0])   # if there are items in the stack ...

    
