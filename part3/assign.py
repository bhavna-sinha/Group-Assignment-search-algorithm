import os
import sys
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
k = 4
m = 5
n = 2

input_file = "E:/IUB/AI/Assignments/Assignment 2/rajthakk-nabiyuni-bhsinha-a1/part3/assign.txt"
#reading from the file
file = open(input_file , 'r')
input_list = []
for line in file:
    input_list.append(line.split())
print(input_list)


pref = {}
non_pref = {}
group_size = {}

for inputlist in range(0, len(input_list)):

    group_size[input_list[inputlist][0]] = int(input_list[inputlist][1])

for inputlist in range(0, len(input_list)):

    if input_list[inputlist][2] == '_':
        pref[input_list[inputlist][0]] = []

    else:

        pref_mem_list = input_list[inputlist][2].split(",")
        pref[input_list[inputlist][0]] = pref_mem_list

for inputlist in range(0, len(input_list)):

    if input_list[inputlist][3] == '_':
        non_pref[input_list[inputlist][0]] = []

    else:

        pref_mem_list = input_list[inputlist][3].split(",")
        non_pref[input_list[inputlist][0]] = pref_mem_list

print()
print()
print(pref)
print(non_pref)
print(group_size)

members = list(pref.keys())
print(members)
initial_teams = [[member] for member in members]
print(initial_teams)

def cost_function(team):
    cost = k
    for member in team:
        if group_size[member] > 0 or group_size[member] != len(team):
            cost += 1
        common_pref = set(pref[member]).intersection(set(team))
        if len(pref[member]) - len(common_pref) > 0:
            cost += (len(pref[member]) - len(common_pref)) * n
        common_non_pref = set(non_pref[member]).intersection(set(team))
        if len(common_non_pref) > 0:
            cost += (len(common_non_pref)) * m
    return cost

q = Q.PriorityQueue()
for initial_team in initial_teams:
    team_cost = cost_function(initial_team)
    q.put((-team_cost, initial_team))

print(q.queue)
total_cost = -sum([e[0] for e in q.queue])
print(total_cost)

new_cost = 0

while(True):
    max_team = q.get()
    team_len = len(max_team)

