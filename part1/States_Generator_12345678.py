def shift_row(state, row, dir):
    change_row = state[(row * 4):(row * 4 + 4)]
    return (state[:(row * 4)] + change_row[-dir:] + change_row[:-dir] + state[(row * 4 + 4):],
            ("L" if dir == -1 else "R") + str(row + 1))


# shift a specified col up (-1) or down ( 1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col + 1))


def successors(state):
    return [shift_row(state, i, d)[0] for i in range(0, 4) for d in (1, -1)] + [shift_col(state, i, d)[0] for i in
                                                                                range(0, 4)
                                                                                for d in (1, -1)]


import time

start_time = time.time()

initial_state = (1, 2, 3, 4, 5, 6, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0)
fringe = [initial_state]
successors_dict = {initial_state: 0}
# fringe = fringe + successors(initial_state)
# print(len(fringe))
# print(len(list((set(fringe)))))

# fringe = list(set(fringe))


# while(len(fringe) > 0):
#     state = fringe.pop()

#     for succ in successors(state):
#         fringe.append(succ)
#         successors_list.append(succ)
#     fringe = list(set(fringe))
#     successors_list = list(set(fringe))
# print(len(successors_list))


while (len(fringe) > 0):
    state = fringe.pop(0)
    #     print('Current state is: ',state)

    for succ in successors(state):

        if succ not in successors_dict:
            fringe.append(succ)
            #     fringe = list(set(fringe))
            successors_dict[succ] = successors_dict[state] + 1
        elif succ in successors_dict:
            old_cost = successors_dict[succ]
            new_cost = successors_dict[state] + 1

            if new_cost < old_cost:
                successors_dict[succ] = successors_dict[state] + 1

    fringe = list(set(fringe))
    #     print('Current fringe is: ', fringe)
    # successors_list = list(set(successors_list))
print(len(successors_dict))

print("--- %s seconds ---" % (time.time() - start_time))

# print(len(successors_list))


board2 = (1, 6, 3, 4, 5, 9, 7, 8, 12, 14, 10, 11, 13, 2, 15, 16)
board4 = (1, 13, 3, 8, 5, 2, 7, 12, 9, 6, 11, 14, 15, 16, 10, 4)
board6 = (15, 13, 3, 8, 12, 1, 2, 7, 5, 6, 11, 14, 9, 16, 10, 4)
board8 = (1, 2, 3, 13, 4, 6, 12, 16, 5, 10, 11, 7, 14, 15, 8, 9)
board12 = (5, 7, 8, 1, 10, 2, 4, 3, 6, 9, 11, 12, 15, 13, 14, 16)

board2_first4 = tuple([element if element in (1, 2, 3, 4, 5, 6, 7, 8) else 0 for element in board2])
board4_first4 = tuple([element if element in (1, 2, 3, 4, 5, 6, 7, 8) else 0 for element in board4])
board6_first4 = tuple([element if element in (1, 2, 3, 4, 5, 6, 7, 8) else 0 for element in board6])
board8_first4 = tuple([element if element in (1, 2, 3, 4, 5, 6, 7, 8) else 0 for element in board8])
board12_first4 = tuple([element if element in (1, 2, 3, 4, 5, 6, 7, 8) else 0 for element in board12])

print(successors_dict[board2_first4])
print(successors_dict[board4_first4])
print(successors_dict[board6_first4])
print(successors_dict[board8_first4])
print(successors_dict[board12_first4])

import pickle

pickle.dump(successors_dict, open("D:\\Artificial Intelligence\\Assignment_1\\successors12345678.p", "wb"))
