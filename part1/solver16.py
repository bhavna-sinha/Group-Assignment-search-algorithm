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
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))


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

def heuristic(state):
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

    range_row_changes = 0
    range_col_changes = 0
    k = 0
    for j in range(0, 16, 4):
        range_row_changes += max(row_changes[j:(j + 4)])-min(row_changes[j:(j + 4)])
        range_col_changes += max(col_changes[k::4])-min(col_changes[k::4])
        k += 1

    # print(range_row_changes)
    # print(range_col_changes)
    result = (range_row_changes+range_col_changes)/4

    return result

def heuristic_trial(state):
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

    range_row_changes = 0
    range_col_changes = 0
    k = 0
    for j in range(0, 16, 4):
        range_row_changes += sum([abs(element) if element !=0 else 0 for element in row_changes[j:(j + 4)]])
        range_col_changes += sum([abs(element) if element !=0 else 0 for element in col_changes[k::4]])
        k += 1

    # print(range_row_changes)
    # print(range_col_changes)
    result = (range_row_changes+range_col_changes)/4

    return result


# The solver! - using BFS right now
def solve(initial_board):
    fringe = [(initial_board, "")]
    fringe_heuristic = [0]
    min_index = 0
    visited = []
    cost = 0

    while len(fringe) > 0:

        (state, route_so_far) = fringe.pop(min_index)
        visited.insert(0,state)
        fringe_heuristic.pop(min_index)
        cost += 1
        #    Modifying the code so that we are using Search Algorithm #2
        if is_goal(state):
            return route_so_far
        for (succ, move) in successors(state):
            # if is_goal(succ):
            #     return( route_so_far + " " + move )
            # if succ not in visited:
            fringe.insert(0, (succ, route_so_far + " " + move))
            fringe_heuristic.insert(0, heuristic(succ)+cost)

        min_value = min(fringe_heuristic)
        min_index = fringe_heuristic.index(min_value)
    return False


# test cases
start_state = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]

# start_state = [1, 13, 3, 8, 5, 2, 7, 12, 9, 6, 11, 14, 15, 16, 10, 4]

if len(start_state) != 16:
    print("Error: couldn't parse start state file")

print("Start state: ")
print_board(tuple(start_state))

print("Solving...")
route = solve(tuple(start_state))

print("Solution found in " + str(len(route) / 3) + " moves:" + "\n" + route)
