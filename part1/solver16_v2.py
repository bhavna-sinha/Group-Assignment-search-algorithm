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








################################## Extra Functions for Heuristic - Start #################################

#Defining the function which will return the moves and directions for each tile in the puzzle to reach goal state

def rows_column_generator(state):
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


    return row_changes, col_changes


# Generating various features for the dataset

def count_positives(state):
    row_changes, col_changes = rows_column_generator(state)

    row_positives = sum([1 for element in row_changes if element > 0])
    col_positives = sum([1 for element in col_changes if element > 0])

    return row_positives, col_positives


def count_negatives(state):
    row_changes, col_changes = rows_column_generator(state)

    row_negatives = sum([1 for element in row_changes if element < 0])
    col_negatives = sum([1 for element in col_changes if element < 0])

    return row_negatives, col_negatives


def rowwise_range(state):
    row_changes, col_changes = rows_column_generator(state)

    row_range = 0
    col_range = 0
    for j in range(0, 16, 4):
        row_range += max(row_changes[j:(j + 4)]) - min(row_changes[j:(j + 4)])
        col_range += max(col_changes[j:(j + 4)]) - min(col_changes[j:(j + 4)])

    return row_range, col_range


def colwise_range(state):
    row_changes, col_changes = rows_column_generator(state)

    row_range = 0
    col_range = 0

    for k in range(0, 4):
        row_range += max(row_changes[k::4]) - min(row_changes[k::4])
        col_range += max(col_changes[k::4]) - min(col_changes[k::4])

    return row_range, col_range


def row_col_range(state):
    row_changes, col_changes = rows_column_generator(state)

    return max(row_changes) - min(row_changes), max(col_changes) - min(col_changes)


def rowwise_max(state):
    row_changes, col_changes = rows_column_generator(state)

    row_max = 0
    col_max = 0
    for j in range(0, 16, 4):
        row_max += max(row_changes[j:(j + 4)])
        col_max += max(col_changes[j:(j + 4)])

    return row_max, col_max


def colwise_max(state):
    row_changes, col_changes = rows_column_generator(state)

    row_max = 0
    col_max = 0
    for k in range(0, 4):
        row_max += max(row_changes[k::4])
        col_max += max(col_changes[k::4])

    return row_max, col_max


def min_row_col(state):
    row_changes, col_changes = rows_column_generator(state)

    return min(row_changes), min(col_changes)


def max_row_col(state):
    row_changes, col_changes = rows_column_generator(state)

    return max(row_changes), max(col_changes)


def rowwise_unique(state):
    row_changes, col_changes = rows_column_generator(state)

    row_unique = 0
    col_unique = 0

    for j in range(0, 16, 4):
        row_unique += len(set(row_changes[j:(j + 4)]))
        col_unique += len(set(col_changes[j:(j + 4)]))

    return row_unique, col_unique


def colwise_unique(state):
    row_changes, col_changes = rows_column_generator(state)

    row_unique = 0
    col_unique = 0

    for k in range(0, 4):
        row_unique += len(set(row_changes[k::4]))
        col_unique += len(set(col_changes[k::4]))

    return row_unique, col_unique


def row_col_unique(state):
    row_changes, col_changes = rows_column_generator(state)

    return len(set(row_changes)), len(set(col_changes))


def summation(state):
    row_changes, col_changes = rows_column_generator(state)

    return sum(row_changes), sum(col_changes)


def abs_summation(state):
    row_changes, col_changes = rows_column_generator(state)

    row_abs_sum = sum([abs(element) for element in row_changes])
    col_abs_sum = sum([abs(element) for element in col_changes])

    return row_abs_sum, col_abs_sum


def dot_row_col(state):
    import numpy as np
    row_changes, col_changes = rows_column_generator(state)

    return np.dot(row_changes, col_changes)


import pickle


def distance_calculator(state):
    #states1234_lookup = pickle.load(
        #open('C:\\Users\\thakk\\Documents\\GitHub\\rajthakk-nabiyuni-bhsinha-a1\\part1\\successors1234.p', "rb"))
    #states5678_lookup = pickle.load(
        #open('C:\\Users\\thakk\\Documents\\GitHub\\rajthakk-nabiyuni-bhsinha-a1\\part1\\successors5678.p', "rb"))
    #states9101112_lookup = pickle.load(
        #open('C:\\Users\\thakk\\Documents\\GitHub\\rajthakk-nabiyuni-bhsinha-a1\\part1\\successors9101112.p', "rb"))
    #states13141516_lookup = pickle.load(
        #open('C:\\Users\\thakk\\Documents\\GitHub\\rajthakk-nabiyuni-bhsinha-a1\\part1\\successors13141516.p', "rb"))

    #state1234 = tuple([element if element in (1, 2, 3, 4) else 0 for element in state])
    #state5678 = tuple([element if element in (5, 6, 7, 8) else 0 for element in state])
    #state9101112 = tuple([element if element in (9, 10, 11, 12) else 0 for element in state])
    #state13141516 = tuple([element if element in (13, 14, 15, 16) else 0 for element in state])

    #d1234 = states1234_lookup[state1234]
    #d45678 = states5678_lookup[state5678]
    #d9101112 = states9101112_lookup[state9101112]
    #d13141516 = states13141516_lookup[state13141516]

    return False, False, False, False


def predictor(state):
    import numpy as np

    row_positives, col_positives = count_positives(state)
    row_negatives, col_negatives = count_negatives(state)

    row_rowwise_range, col_rowwise_range = rowwise_range(state)
    row_colwise_range, col_colwise_range = colwise_range(state)

    row_range, col_change = row_col_range(state)

    row_rowwise_max, col_rowwise_max = rowwise_max(state)
    row_colwise_max, col_colwise_max = colwise_max(state)

    row_min, col_min = min_row_col(state)
    row_max, col_max = max_row_col(state)

    row_rowise_unique, col_rowwise_unique = rowwise_unique(state)
    row_colwise_unique, col_colwise_unique = colwise_unique(state)

    row_unique, col_unique = row_col_unique(state)

    row_sum, col_sum = summation(state)

    row_abs_sum, col_abs_sum = abs_summation(state)

    dot_product = dot_row_col(state)

    d1234, d45678, d9101112, d13141516 = distance_calculator(state)

    X = [1, row_positives, col_positives, row_negatives, col_negatives, row_rowwise_range, col_rowwise_range,
         row_colwise_range, col_colwise_range, row_range, col_change, row_rowwise_max, col_rowwise_max,
         row_colwise_max, col_colwise_max, row_min, col_min, row_max, col_max, row_rowise_unique, col_rowwise_unique,
         row_colwise_unique, col_colwise_unique, row_unique, col_unique, row_sum, col_sum, row_abs_sum, col_abs_sum,
         dot_product, d1234, d45678, d9101112, d13141516]

    theta = [5.48491064e-02, -7.12614119e-03, -3.68746606e-04, 4.66991625e-02,
             -9.73031963e-03, -1.52116506e-01, -1.00990662e-02, -5.67250132e-02,
             0.00000000e+00, -1.41812533e-02, -2.52476656e-03, -4.91889192e-02,
             -3.68746606e-04, -4.62175721e-02, 2.34039326e-03, 2.62686028e-03,
             2.43257991e-03, -1.15543930e-02, -9.21866515e-05, 2.39984608e-01,
             2.09297359e-01, 6.28569460e-02, 2.19396426e-01, 1.57142365e-02,
             5.23243398e-02, 1.07477335e-01, 9.36157302e-03, 2.00875660e-01,
             -1.00990662e-02, -3.33161735e-02, 3.00988781e-02, 1.27343899e-01,
             -7.03165478e-02, -4.70063803e-02]

    return round(np.dot(X, theta), 2)


################################## Extra Functions for Heuristic - End ###################################

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
                hs = (heuristic1(succ_city)+heuristic2(succ_city))/2#heurisitc func
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
