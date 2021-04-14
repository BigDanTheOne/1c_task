from copy import deepcopy

increasing_matchings = {'6' : '7', '7' : '8', '8' : '9', '9' : '10',
             '10' : 'В', 'В' : 'Д', 'Д' : 'К', 'К' : 'Т'}

decreasing_matchings = {'Т' : 'К', 'К' : 'Д', 'Д' : 'В', 'В' : '10',
                        '10' : '9', '9' : '8', '8' : '7', '7' : '8'}
def write_hash(state):
    ans = ""
    for i in state.stacks:
        for j in i:
            ans += j
        ans += ';'
    return ans

class State:
    def __init__(self, stacks):
        self.stacks = stacks
        self.closed = [(len(stacks[0]) - 2) for i in range(len(stacks))]

    def __hash__(self):
        _hash = 0

        for stack in self.stacks:
            _hash ^= hash(tuple(stack))

        return _hash ^ hash(tuple(self.closed))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

def read_table():
    ans = []
    for i in range(3):
        heap = []
        for j in range(2):
            s = input()
            #if j == 1:
            #    heap += ['|']
            heap += [s]
        ans += [heap]
    return ans

def calculate_heuristic(state : State):
    ans = 0
    stacks = state.stacks
    closed = state.closed
    for i in range(len(stacks)):
        stack_i = stacks[i]
        ans += len(stack_i)
        ordered_row_len = 0
        for j in range(closed[i] + 1): ## increasing order
            if j < closed[i] - 1 and stack_i[j] == increasing_matchings[stack_i[j + 1]]:
                ordered_row_len += 1
            else:
                ans += ordered_row_len
                ordered_row_len = 0
        ans += ordered_row_len
        ordered_row_len = 0
        for i in range(closed[i] + 1, len(stack_i)): ## decreasing order
            if j < len(stack_i) - 1 and stack_i[j] == decreasing_matchings[stack_i[j + 1]]:
                ordered_row_len += 1
            else:
                ans += ordered_row_len
                ordered_row_len = 0
        ans += ordered_row_len
    return ans

def parse_hash(hashed_state):
    ans = []
    end_of_heap_indx = hashed_state.find(';')
    while end_of_heap_indx != -1:
        hased_heap = hashed_state[:end_of_heap_indx]
        heap = []
        for i in hased_heap:
            if i == '0':
                heap += ['10']
            elif i == '1':
                continue
            else:
                heap += [i]
        ans += [heap]
        hashed_state = hashed_state[end_of_heap_indx + 1:]
        end_of_heap_indx = hashed_state.find(';')
    return ans

def check(line):
    return line == ['Т', 'К', 'Д', 'В', '10', '9', '8', '7', '6']

def find_neighbors(current_state : State):
    neighbours = []
    #current_state = parse_hash(hashed_current_state)
    stacks = current_state.stacks
    closed = current_state.closed
    for i in range(len(stacks)):
        for j in reversed(range(len(stacks[i]))):
            if j == closed[i]:
                break
            curr_symbol = stacks[i][j]
            for k in range(len(stacks)):
                if len(stacks[k]) != 0 and increasing_matchings[curr_symbol] == stacks[k][-1]:
                    new_state = deepcopy(current_state)
                    new_state.stacks[k] += stacks[i][j:]
                    new_state.stacks[i] = stacks[i][:j]
                    if check(new_state.stacks[k][-9:]):
                        new_state.stacks[k] = new_state.stacks[k][:-9]

                    if (j - 1) == new_state.closed[i]:
                        new_state.closed[i] -= 1
                    neighbours += [new_state]
    return neighbours

def solve(start, finish):
    to_consider = set()
    was_considered = set()
    cost = dict()
    heuristic = dict()

    cost[start] = 0
    heuristic[start] = cost[start] + calculate_heuristic(start)
    to_consider.add(start)
    while len(to_consider) != 0:
        current_state = min(to_consider, key = lambda x : heuristic[x])
        if current_state.stacks == finish.stacks:
            return True
        to_consider.remove(current_state)
        was_considered.add(current_state)
        for neighbour_state in find_neighbors(current_state):
            trial = cost[current_state] + 1
            if neighbour_state in was_considered and trial >= cost[neighbour_state]:
                continue
            else:
                cost[neighbour_state] = trial
                heuristic[neighbour_state] = cost[neighbour_state] + calculate_heuristic(neighbour_state)
                if neighbour_state not in to_consider:
                    to_consider.add(neighbour_state)
    return False

# ТЕСТОВЫЙ ПРИМЕР
start = State([['Т'], ['6', '7', '8', '9', '10', 'В', 'Д', 'К']])
start.closed = [0, 7]
final = State([[], []])
final.closed = [-1, -1]
print(solve(start, final))

print(solve(State(read_table()), final))
