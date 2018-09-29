#!/bin/python3
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#

import heapq
import numpy as np


def X_Y_cal(state):
    state = np.array(state).reshape(4, -1)
    des_state = np.arange(16).reshape(4, -1)
    map = {}
    for r_ind, row in enumerate(des_state):
        for c_ind, col in enumerate(row):
            map[col + 1] = [r_ind, c_ind]
    row_changes, col_changes = np.zeros((4, 4), dtype=int), np.zeros((4, 4), dtype=int)
    for r_ind, row in enumerate(state):
        for c_ind, col in enumerate(row):
            # row_changes[map[col][0]][map[col][1]] = ((map[col][1] - c_ind) + 4) % 4
            # col_changes[map[col][0]][map[col][1]] = ((r_ind - map[col][0]) + 4) % 4
            row_changes[r_ind][c_ind] = ((map[col][1] - c_ind) + 4) % 4
            col_changes[r_ind][c_ind] = ((r_ind - map[col][0]) + 4) % 4
    return row_changes, col_changes

# shift a specified row left (-1) or right (1)
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


# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print('%3d %3d %3d %3d' % (row[j:(j + 4)]))


# return a list of possible successor states
def successors(state):
    return [shift_row(state, i, d) for i in range(0, 4) for d in (1, -1)] + [shift_col(state, i, d) for i in range(0, 4)
                                                                             for d in (1, -1)]



def print_tables(state):
    row_changes, col_changes = X_Y_cal(state)
    # print(np.array(state).reshape(4,-1))
    print()
    print(row_changes)
    print(col_changes)

def my_heuristic(state):
    # row_changes, col_changes = rows_column_generator(state)
    row_changes, col_changes = X_Y_cal(state)
    # print_tables(state)
    s = 0
    for ind, row in enumerate(row_changes):
        set_m = set(row) - set([0])
        s += pow(len(set_m), 1)

    for ind, row in enumerate(np.transpose(col_changes)):
        set_m = set(row) - set([0])
        s += pow(len(set_m), 1)

        #   my tries for finding the heuritic
        # binar = [1 if x != 0 else 0 for x in row]
        # # s += sum(binar)
        # m = np.max(row)
        # n = np.min(row)
        # set_m = [m - x for x in set_m]
        # # s += m
        # # s -= n
        # # s += sum(set_m)
        # # s += sum(row)

    return s

def astar_search(start_city, end_city, use_heurisitc):
    closed = {}
    path = []
    hs = 0
    fringe = [(hs, start_city)]
    heapq.heapify(fringe)
    closed[start_city] = ["-1", 0, ""]
    while len(fringe) > 0:
        city = heapq.heappop(fringe)
        city = city[1]
        # path.append(move)
        if (city == end_city):
            return path, closed
        city_d = closed[city][1] # city_d is the same as g(s) in this case
        for ind, item in enumerate(successors(city)):
            succ_city = item[0]
            move = item[1]
            if succ_city in closed and closed[succ_city][1] <= city_d + 1:
                continue
            closed[succ_city] = [city, city_d + 1, move] # Marking visited cities to avoid infinite-loops
            hs = 0
            if use_heurisitc: # defining h(s): heuristic function
                # heuristic 1
                hs = my_heuristic(succ_city) / 2#(heuristic1(succ_city)+heuristic2(succ_city))/2#heurisitc func
            heapq.heappush(fringe, (city_d + 1 + hs, succ_city))

    return [], {}



start_state = [1 ,6 ,3 ,4 ,5 ,9 ,7 ,8 ,12 ,14 ,10 ,11 ,13 ,2, 15, 16] # board 2
print_tables(start_state)
print(my_heuristic(start_state))

start_state = [1, 13, 3, 8, 5, 2, 7, 12, 9, 6, 11, 14, 15, 16, 10, 4 ] # board 4
print_tables(start_state)
print(my_heuristic(start_state))

start_state = [15, 13, 3, 8, 12, 1, 2, 7,  5, 6, 11, 14, 9, 16, 10, 4] # board 6
print_tables(start_state)
print(my_heuristic(start_state))

start_state = [5, 7, 8, 1, 10, 2, 4, 3, 6, 9, 11, 12, 15, 13, 14, 16] # board 12
print_tables(start_state)
print(my_heuristic(start_state))
# start_state = [2, 13, 14, 1, 6, 7, 3, 5, 9, 10, 8, 12, 15, 4, 11, 16] # board 8


if len(start_state) != 16:
    print("Error: couldn't parse start state file")

print("Start state: ")
print_board(tuple(start_state))

print("Solving...")
goal_board = tuple(sorted(tuple(start_state)))

import time

start_time = time.time()

path, closed = astar_search(tuple(start_state), goal_board,True)
if closed != {}: print("SUCCESS")
else: print("No answer!")


b = goal_board
a = closed[b][0]
move = closed[b][2]
best_path = [move]
while(a != "-1"):
    best_path.insert(0, closed[a][2])
    b = a
    a = closed[a][0]


print("--- %s seconds ---" % (time.time() - start_time))

print('Solution found in ',len(best_path[1:]),'moves')
print(' '.join(best_path[1:]))