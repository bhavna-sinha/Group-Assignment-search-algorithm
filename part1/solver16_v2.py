#!/usr/bin/env python3
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#
# Changed Queue to queue for python3
from queue import PriorityQueue
from random import randrange, sample
import sys
import string
import operator
import heapq
import pickle
import time
import numpy as np


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


# just reverse the direction of a move name, i.e. U3 -> D3
# def reverse_move(state):
#     return state.translate(string.maketrans("UDLR", "DURL"))


# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)


# defining the heuristic function

# def heuristic(state):
#     desired_state = sorted(state)
#     count_row = 0
#     count_col = 0
#     k = 0
#     for j in range(0, 16, 4):
#         count_row += 4 - len(set(state[j:(j + 4)]).intersection(set(desired_state[j:(j + 4)])))
#         count_col += 4 - len(set(state[k::4]).intersection(set(desired_state[k::4])))
#         k += 1
#     # print(count_row)
#     # print(count_col)
#
#     return (count_row/4) + (count_col/1.5)

def heuristic1(state):
    desired_state = sorted(state)
    cordinates = []
    col_changes = []
    row_changes = []
    for i in range(4):
        for j in range(4):
            cordinates.append((i,j))
    for i in range(len(state)):
        ind = desired_state.index(state[i])
        cordinates_state = cordinates[i]
        cordinates_desired_state = cordinates[ind]

        col = cordinates_desired_state[0] - cordinates_state[0]
        row = cordinates_desired_state[1] - cordinates_state[1]

        if col == 3:
            col_changes.append(-1)
        elif col == -3:
            col_changes.append(1)
        elif col == -2 or col == 2:
            col_changes.append(2)
        else:
            col_changes.append(col)

        if row == 3:
            row_changes.append(-1)
        elif row == -3:
            row_changes.append(1)
        elif row == -2 or row == 2:
            row_changes.append(2)
        else:
            row_changes.append(row)

        result_row = sum([abs(element) for element in row_changes])
        result_col = sum([abs(element) for element in col_changes])

    return (result_row+result_col)/4

def heuristic2(state):
    desired_state = sorted(state)
    cordinates = []
    col_changes = []
    row_changes = []
    for i in range(4):
        for j in range(4):
            cordinates.append((i,j))
    for i in range(len(state)):
        ind = desired_state.index(state[i])
        cordinates_state = cordinates[i]
        cordinates_desired_state = cordinates[ind]

        col = cordinates_desired_state[0] - cordinates_state[0]
        row = cordinates_desired_state[1] - cordinates_state[1]

        if col == 3:
            col_changes.append(-1)
        elif col == -3:
            col_changes.append(1)
        elif col == -2 or col == 2:
            col_changes.append(2)
        else:
            col_changes.append(col)

        if row == 3:
            row_changes.append(-1)
        elif row == -3:
            row_changes.append(1)
        elif row == -2 or row == 2:
            row_changes.append(2)
        else:
            row_changes.append(row)

        result_row = 0
        result_col = 0



    for i in range(len(row_changes)):
        x = abs(row_changes[i])
        y = abs(col_changes[i])
        if x != 0 and y != 0:
            if x == 1 and y == 1:
                result_row += x/4
                result_col += y/4
            if x == 2 and y == 2:
                result_row += x/2
                result_col += y/2
            else:
                result_row += x/1.5
                result_col += y/1.5
        else:

            result_row += x/8
            result_col += y/8

    return (result_row+result_col)/2

def my_heuristic(state):
    # row_changes, col_changes = rows_column_generator(state)

    desired_state = sorted(state)
    cordinates = []
    col_changes = []
    row_changes = []
    for i in range(4):
        for j in range(4):
            cordinates.append((i, j))
    for i in range(len(state)):
        ind = desired_state.index(state[i])
        cordinates_state = cordinates[i]
        cordinates_desired_state = cordinates[ind]

        col = cordinates_desired_state[0] - cordinates_state[0]
        row = cordinates_desired_state[1] - cordinates_state[1]

        if col == 3:
            col_changes.append(-1)
        elif col == -3:
            col_changes.append(1)
        elif col == -2 or col == 2:
            col_changes.append(2)
        else:
            col_changes.append(col)

        if row == 3:
            row_changes.append(-1)
        elif row == -3:
            row_changes.append(1)
        elif row == -2 or row == 2:
            row_changes.append(2)
        else:
            row_changes.append(row)

    # print(row_changes)

    # row_changes_array = np.array(row_changes).reshape(4, -1)
    # print(row_changes_array)
    # col_changes_array = np.array(col_changes).reshape(4, -1)
    # print(col_changes_array)
        # row_changes = np.reshape(row_changes,(-1,4))
        # col_changes = np.array(col_changes)
        # col_changes = np.reshape(col_changes,(-1,4))

    row_unique = 0
    col_unique = 0

    for j in range(0, 16, 4):
        row_unique_set = set(row_changes[j:(j + 4)]) - set([0])
        row_unique += len(row_unique_set)
        # print(row_unique)

        # col_unique_set = set(col_changes[j:(j + 4)]) - set([0])
        # col_unique += len(col_unique_set)
    for k in range(0, 4):
        # row_unique_set = set(col_changes[k::4]) - set([0])
        col_unique_set = set(col_changes[k::4]) - set([0])

        # row_unique += len(row_unique_set)
        col_unique += len(col_unique_set)



    # row_changes, col_changes = X_Y_cal(state)
    # print_tables(state)
    # s = 0
    # for ind, row in enumerate(row_changes):
    #     set_m = set(row) - set([0])
    #     s += pow(len(set_m), 1)
    #
    # for ind, row in enumerate(np.transpose(col_changes)):
    #     set_m = set(row) - set([0])
    #     s += pow(len(set_m), 1)

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

    return (((row_unique+col_unique)**1.1)*0.85)/2


##########################Iman's COde###############################################

#start_city = initial_board
#end_city = Goal_Board
#road_hash_Map  = successor_function
# cost_function = "segments"

# astar_search(,,,"segments",)
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
                # hs = (0.5*heuristic1(succ_city)+0.5*heuristic2(succ_city))#heurisitc func
                hs = my_heuristic(succ_city)
            heapq.heappush(fringe, (city_d + 1 + hs, succ_city))

    return [], {}

####################################################################################










# The solver! - using BFS right now
# def solve(initial_board):
#     fringe = []
#     # fringe_dict = {}
#     closed = []
#     fringe.append((initial_board,""))
#     heuristic_fringe = [0]
#     cost_fringe = [0]
#
#
#     cost = 0
#
#
#     while len(fringe) > 0:
#         min_value = min(heuristic_fringe)
#         min_index = heuristic_fringe.index(min_value)
#         (state, route_so_far) = fringe.pop(min_index)
#         heuristic_fringe.pop(min_index)
#
#         closed.append(state)
#         # cost_fringe.append(cost_fringe[min_index]+1)
#
#         if is_goal(state):
#             return route_so_far
#
#         for (succ,move) in successors(state):
#             # if succ in closed:
#             #     continue
#             if succ in fringe:
#                 new_cost = cost + heuristic(succ)
#                 old_cost = heuristic_fringe[fringe.index(succ)]
#
#                 if new_cost < old_cost:
#                     i = fringe.index(succ)
#                     fringe.remove(succ)
#                     heuristic_fringe.pop(i)
#                     fringe.append([succ, route_so_far + " " + move])
#                     heuristic_fringe.append(new_cost)
#             elif succ not in fringe:
#                 fringe.append([succ, route_so_far + " " + move])
#                 heuristic_fringe.append(heuristic(succ)+cost)
#
#
#
#     return False


# test cases
start_state = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]

# start_state = [1, 13, 3, 8, 5, 2, 7, 12, 9, 6, 11, 14, 15, 16, 10, 4]
# start_state = [1, 2, 3, 13, 4, 6, 12, 16, 5, 10, 11, 7, 14, 15, 8, 9]
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


# print("Solution found in " + str(len(route) / 3) + " moves:" + "\n" + route)
