#!/bin/python3

"""
To solve this problem first we formulated the problem in this manner:
Set of Valid states: All available cities in the map would be our valid states. Successor function will return a subset
of this set at any time.

Initial State: The initial state of the map is a city that the path would start from that point.

Successor function: This function is a function that would return all neighbors of a given city. These neighbors are all
the possible states we can go from a given city.

Cost function/edge weights: Cost function can has three possible values. Distance would be the distance in miles
between two cities. In this case the distance values from road-segment file would be considered as edge weights. Time is
another possible cost function which will be the traveling time from one city to another one and is the division of
distance by the speed limit between cities. Segments are number of cities that we path and in this case edge
weight for each pair of cities would be considered a constant value(e.g. 1).

Goal state: The goal state is the end-city that we want to arrive. This city is the last city at the end of our path.

Heuristic function: This function is just get calculated for astar routing algorithm and is the distance between current
 city and the end-city that we want to reach. This distance is calculated by using latitude and longitude of current city
 and end-city. As it is mentioned in the assumption section, for those cities which are not in the city-gps file,
 a high priority(i.e. a low heuristic function) will be considered to make sure that they would be considered in
 the process of finding the best path. In other words, as our best path may go through one of these cities without
 gps values, we always considered them and remove them first from the fringe to make sure we are not missing any possible
 candidate for the best route.
We tested three different heuristic functions and we used the first one which is admissible for distance:

1. Real distance in miles: By using Haversine formula we can calculate the distance of two cities in miles. This function
is admissible if the cost function is distance, because the closest distance between two cities is the distance that
directly connect them to each-other. So this function always underestimates the distance between two cities.
In other words, all the paths would have equal or larger distance than the result of the function. So we can say that
astar search for distance cost function is optimal.
For any other cost function, this function is not admissible and as a result the result the astar search is not optimal.
The reason is that this function calculate the cost and not time or number of segments. We may argue that it would be
hard or so expensive to have a admissible function for time. The reason is that we may get closer to a city but the path
takes more time than another path which is longer because of the speed limits. In other words the travel time is not
consistent across the cities, so it would be hard to find a admissible function for that. A similar argument applies for
segments cost function.

2. Manhattan distance in degrees: by using differences of latitude and longitude of the two cities in degrees, we can
calculate distance based on degrees instead of miles. This function is not admissible for non of the cost functions
because the different between angle of two cities(i.e. latitude) are larger near the equator and smaller near the pole.

3. Euclidean Distance: by using differences of latitude and longitude of the two cities in degrees, we can calculate
distance based on degrees instead of miles. This function is not admissible for non of the cost functions because
the different between angle of two cities(i.e. latitude) are larger near the equator and smaller near the pole.

How the search algorithm works:
For bfs, dfs and ids routing algorithms, the program uses a function named blind_search which adds all possible successors
to a fringe data-set and start popping them based of the type of routing algorithm (i.e. queue for bfs and stack for dfs}.
ids search would call dfs search and limits its search to a specific depth. The depth would increase after each failure
up to the depth 1000. After this depth the program will return "No Path has found!!!" and will terminate the search.
For uniform and astar routing algorithms, another function named astar_search will be called. This function uses a
priority queue to simulate best first search and pop a city with the lowest evaluation function value (i.e. f(s)).
Value of g(s)(which is the first part of f(s)) depends on the type of cost function. It will be the cost of reaching to
the current point by considering all costs(edge weights) along the path.
However, the second term of f(s) (which is h(s)) would depend of the type of routing algorithm. For uniform search
the function assume a zero value for heuristic function and for astar search it will use the first heuristic which was
described before.

Problems we faced, any assumptions, simplifications, and/or design decisions:
Assumptions:
- The start-city and end-city are in the city-gps file. In this way we would make sure that our heuristic function would
always have a second point for calculation.
- Cities with missing gps in the path have high priority.
- We can skip a revisit city which was visited through a shorter path before. This means that all possible successors
of that city considering the shorter path were examined before. So there is no way of missing a possible best path by
using this approach.
Problems we faced:
- Some of the gps in the city-gps file for some cities are missing. This means that we cannot calculate heuristic function
accurately for the current city. To face this problem, we assumed that the heuristic for such a city is minimum value.
This would guarantee that this city would not lose the chance of being removed from the fringe and we would not miss
any possible candidate for the best route.
- Some of the highways do not have speed limit. To solve this problem we ignore those highway so they would not show
in our best found paths as an answer.
Design decisions:
- To make the code shorter we used one function for couple of routing algorithm and one function for calculating g(s)
of any given cost. This would make debugging and reading easier.
- Visualization of the path is possible by adding one extra word "yes" at the end of the input arguments for
calling the rout.py file. This helps to find any possible pitfalls or bugs and understand the way that
algorithm works.

"""


import pandas as pd
import numpy as np
from sys import argv, exit, setrecursionlimit
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
import heapq
from math import sin, cos, sqrt, atan2

# setrecursionlimit(5000)

def load_data(data_path, seprt):
    unarng_data = pd.read_table(data_path, sep=seprt, header=None)
    unarng_data = unarng_data.values
    return unarng_data

def draw_plot(path, closed, city_pos_map, routing_algorithm, cost_function, best_path):
    blit = False#True#
    draw_dots = False#True#
    print_text = False#True#True#
    fig_m, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5 * 3, 5 * 3))
    plt.rcParams.update({'font.size': 6})
    fig_m.tight_layout(rect=[0.025, 0.025, 0.95, 0.95])
    # fig_m.subplots_adjust(hspace=.1)
    ax0 = plt.subplot(111)#, sharex=ax0)
    min_x, max_x, min_y, max_y = 1000, -1000, 1000, -1000
    city = path[-1]
    ind = len(path)
    while (city != "-1"):
        if city in city_pos_map:
            coord = city_pos_map[city]
            min_x = min(min_x, coord[0])
            max_x = max(max_x, coord[0])
            min_y = min(min_y, coord[1])
            max_y = max(max_y, coord[1])

        if draw_dots:
            if ind >= 0:
                ind -= 1
                city = path[ind]
            else:
                city = "-1"
        elif not draw_dots:
            city = closed[city][0]

    ax0.set_xlim(min_x, max_x)
    ax0.set_ylim(min_y, max_y)
    ax0.xaxis.set_major_locator(ticker.LinearLocator(20))
    ax0.xaxis.set_minor_locator(ticker.LinearLocator(20))
    ax0.xaxis.grid(True, linestyle='--', which='major', color='black', alpha=1.0)
    ax0.yaxis.grid(True, linestyle='--', which='major', color='black', alpha=1.0)
    ax0.set_ylabel('longitude')
    ax0.set_xlabel('latitude')
    ax0.set_title('Map of cities- Path length: %d' % (closed[path[-1]][1] + 1))
    # for key in city_pos_map.keys():
    #     ax0.text(city_pos_map[key][0], city_pos_map[key][1], key.split(',')[0], ha='center')

    if blit: fig_m.canvas.draw()

    # Printing city names from start to end city
    x, y = 40, -100
    for ind, key in enumerate(best_path):
        offset = int(ind / 200) * 200
        C = np.array([0 + ind - offset, 0 + ind - offset, 255])
        if key in city_pos_map:
            x = city_pos_map[key][0]
            y = city_pos_map[key][1]
        else:
            y += 0.1
        ax0.text(x, y, key.split(',')[0], ha='center', color=C/255.0)
        plt.pause(1e-10)

    key = path[0]
    if key in city_pos_map:
        ax0.text(city_pos_map[key][0], city_pos_map[key][1], key.split(',')[0], ha='center', color='red', weight='bold')
    else:
        ax0.text(40, -100, city.split(',')[0], ha='center', color='red', weight='bold')

    key = path[-1]
    if key in city_pos_map:
        ax0.text(city_pos_map[key][0], city_pos_map[key][1], key.split(',')[0], ha='center', color='green', weight='bold')
    else:
        ax0.text(40, -100, city.split(',')[0], ha='center', color='green', weight='bold')
    plt.pause(1e-100)

    if blit: axbackground = fig_m.canvas.copy_from_bbox(ax0.bbox)
    if draw_dots:
        x, y = 40, -100
        for ind, key in enumerate(path[1:-1]):
            offset = int(ind / 200) * 200
            C = np.array([0 + ind - offset, 0 + ind - offset, 255])
            if key in city_pos_map:
                x = city_pos_map[key][1]
                y = city_pos_map[key][0]
            else:
                y += 0.1
            if print_text:
                ax0.text(x, y, key.split(',')[0], ha='center', color=C/255.0)
            else:
                ax0.scatter(x, y, c=C/255.0, marker='o')#

            if blit:
                fig_m.canvas.restore_region(axbackground)
                fig_m.canvas.blit(ax0.bbox)
            plt.pause(1e-10)

    plt.savefig("path_from_%s_to_%s_%s_%s" % (path[0], path[-1], routing_algorithm, cost_function))#, bbox_inches='tight')
    plt.show()
    return best_path

def cal_depth(closed, city):
    d = 0
    while city != "-1":
        d += 1
        city = closed[city]
    return d

def cal_cost(co, a, b, dist_map):
    if co == "segments": return 1
    if a+b in dist_map: return dist_map[a+b][0] / 10 if co == "distance" else 5 * dist_map[a+b][0] / (dist_map[a+b][1])# if dist_map[a+b][1] > 0 else 25)
    elif b+a in dist_map: return dist_map[b+a][0] / 10 if co == "distance" else 5 * dist_map[b+a][0] / (dist_map[b+a][1])# if dist_map[b+a][1] > 0 else 25)
    print("WRONG COST CAL!!!")
    return 1000
def cal_dist(lat1, lon1, lat2, lon2):
    R = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


def print_results(path, closed, routing, co, dist_map):
    output = "no" if routing == "dfs" or (routing in ["bfs", "ids"] and co != "segments") \
                     or (routing == "astar" and co != "distance") \
        else "yes"
    distance, time = 0, 0
    b = path[-1]
    a = closed[b][0]
    best_path = [b]
    while(a != "-1"):
        if a+b in dist_map:
            distance += dist_map[a+b][0] / 10
            time += dist_map[a+b][0] / (dist_map[a+b][1] if dist_map[a+b][1] > 0 else 25)
        elif b+a in dist_map:
            distance += dist_map[b+a][0] / 10
            time += dist_map[b+a][0] / (dist_map[b+a][1] if dist_map[b+a][1] > 0 else 25)

        best_path.insert(0, a)
        b = a
        a = closed[a][0]

    # print("Path length: ", closed[path[-1]][1])
    print("Best Path with %d cities:" % len(best_path))# + "\t".join(best_path))

    output += " %d %0.4f " % (distance * 10, time) + " ".join(best_path)
    print(output)
    return best_path

def blind_search(start_city, end_city, road_hash_Map, routing_algorithm, cost_function, highway_dist_map, d = None):
    closed = {}
    path = []
    pop_pos = -1 if (routing_algorithm == "dfs") else 0
    fringe = [start_city]
    closed[start_city] = ["-1", 0]
    while len(fringe) > 0:
        city = fringe.pop(pop_pos)
        path.append(city)
        if (city == end_city):
            return path, closed
        city_d = closed[city][1]
        if(d == None or city_d <= d): # To make sure ids will not pass depth d
            for ind, succ_city in enumerate(road_hash_Map[city]):
                if (succ_city in closed and d == None) or (succ_city in closed and closed[succ_city][1] <= city_d + 1):
                    continue
                closed[succ_city] = [city, city_d + 1] # Marking visited cities to avoid infinite-loops

                fringe.append(succ_city)

    return [], {}

def astar_search(start_city, end_city, road_hash_Map, cost_function, city_pos_map, highway_dist_map, use_heurisitc):
    closed = {}
    path = []
    hs = abs(city_pos_map[start_city][0] - city_pos_map[end_city][0]) +\
         abs(city_pos_map[start_city][1] - city_pos_map[end_city][1])
    fringe = [(hs, start_city)]
    heapq.heapify(fringe)
    closed[start_city] = ["-1", 0]
    while len(fringe) > 0:
        city = heapq.heappop(fringe)
        city = city[1]
        path.append(city)
        if (city == end_city):
            return path, closed
        city_d = closed[city][1] # city_d is the same as g(s) in this case
        for ind, succ_city in enumerate(road_hash_Map[city]):
            if succ_city in closed and closed[succ_city][1] <= city_d + cal_cost(cost_function, city, succ_city, highway_dist_map):
                continue
            closed[succ_city] = [city, city_d + cal_cost(cost_function, city, succ_city, highway_dist_map)] # Marking visited cities to avoid infinite-loops

            hs = 0
            if use_heurisitc and (succ_city in city_pos_map): # defining h(s): heuristic function
                # heuristic 1
                hs = cal_dist(city_pos_map[succ_city][0], city_pos_map[succ_city][1], city_pos_map[end_city][0], city_pos_map[end_city][1]) / 880
                # heuristic 2
                # hs = abs(city_pos_map[succ_city][0] - city_pos_map[end_city][0]) + abs(city_pos_map[succ_city][1] - city_pos_map[end_city][1])
                # heuristic 3
                # hs = sqrt(pow(abs(city_pos_map[succ_city][0] - city_pos_map[end_city][0]), 2) + pow(abs(city_pos_map[succ_city][1] - city_pos_map[end_city][1]), 2))
            heapq.heappush(fringe, (city_d + cal_cost(cost_function, city, succ_city, highway_dist_map) + hs * 2, succ_city))

    return [], {}

def main_search(start_city, end_city, road_hash_Map, routing_algorithm, cost_function, city_pos_map, highway_dist_map):
    if routing_algorithm in ["dfs", "bfs"]: return blind_search(start_city, end_city, road_hash_Map, routing_algorithm, cost_function, highway_dist_map)
    elif routing_algorithm == "ids":
        path = []
        closed = {}
        d = 0
        while path == [] and d < 1000:
            path, closed = blind_search(start_city, end_city, road_hash_Map, "dfs", cost_function, highway_dist_map, d)
            d += 1
        return path, closed
    elif routing_algorithm in ["uniform", "astar"]:
        use_heuristic = True if routing_algorithm == "astar" else False
        return astar_search(start_city, end_city, road_hash_Map, cost_function, city_pos_map, highway_dist_map, use_heuristic)
    return [], {}
if __name__ == "__main__":
    start_city, end_city, routing_algorithm, cost_function = "", "", "", ""
    show_plot = False
    try:
        args = iter(argv)
        next(args)
        start_city = next(args)
        end_city = next(args)
        routing_algorithm = next(args)
        cost_function = next(args)
    except:
        print("NOT ENOUGH INPUTS!!!")

    try:
        show_plot = True if next(args) == "yes" else print("You did not ask for a visualized plot of the route!")
    except:
        print("You did not ask for a visualized plot of the route!")

    if cost_function not in ["time", "distance", "segments"] or\
       routing_algorithm not in ["bfs", "dfs", "ids", "astar", "uniform"]:
        print("WRONG INPUTS!!!")
        exit()
    road_segments = load_data("./road-segments.txt", " ")
    city_gps = load_data("./city-gps.txt", " ")
    city_pos_map = {}
    for city, lat, lon in city_gps:
        city_pos_map[city] = [lat, lon]
    road_hash_Map = {}
    highway_dist_map = {}
    for highway in road_segments:
        if len(highway) < 4 or highway[3] == 0: # Skipping highways with 0 speed limit as was suggested in piazza
            continue
        key = highway[0]#.split(',')[0]
        value = highway[1]#.split(',')[0]
        highway_dist_map[key+value] = highway[2:4]
        if key not in road_hash_Map: road_hash_Map[key] = [value]
        else: road_hash_Map[key].append(value)
        if value not in road_hash_Map: road_hash_Map[value] = [key]
        else: road_hash_Map[value].append(key)
    path, closed = main_search(start_city, end_city, road_hash_Map, routing_algorithm, cost_function, city_pos_map, highway_dist_map)
    if path == []:
        print("No Path has found!!!")
        exit()
    best_path = print_results(path, closed, routing_algorithm, cost_function, highway_dist_map)
    if show_plot:
        draw_plot(path, closed, city_pos_map, routing_algorithm, cost_function, best_path)
