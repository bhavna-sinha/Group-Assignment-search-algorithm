#!/bin/python
import pandas as pd
import numpy as np
from sys import argv, exit, setrecursionlimit
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
import heapq

setrecursionlimit(5000)

def load_data(data_path, seprt):
    unarng_data = pd.read_table(data_path, sep=seprt, header=None)
    unarng_data = unarng_data.values
    return unarng_data

def draw_plot(path, closed, city_pos_map, routing_algorithm, cost_function):
    best_path = []
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

    key = path[-1]
    ind = 0
    x, y = 40, -100
    while(key != "-1"):
        offset = int(ind / 200) * 200
        C = np.array([0 + ind - offset, 0 + ind - offset, 255])
        if key in city_pos_map:
            x = city_pos_map[key][0]
            y = city_pos_map[key][1]
        else:
            y += 0.1
        ax0.text(x, y, key.split(',')[0], ha='center', color=C/255.0)
        plt.pause(1e-10)
        best_path.append(key)
        key = closed[key][0]
        ind += 1

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
                x = city_pos_map[key][0]
                y = city_pos_map[key][1]
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

def blind_search(start_city, end_city, road_hash_Map, routing_algorithm, cost_function, d = None):
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
                if succ_city not in closed: closed[succ_city] = [city, city_d + 1] # Marking visited cities to avoid infinite-loops
                else:
                    if d != None and closed[succ_city][1] > closed[city][1] + 1: # To update in ids cities with recently found shorter path
                        closed[succ_city] = [city, closed[city][1] + 1]
                    else:
                        continue
                fringe.append(succ_city)

    return [], {}

def astar_search(start_city, end_city, road_hash_Map, cost_function, closed, path, city_pos_map):
    fringe = []
    heapq.heapify(fringe)
    city_d = closed[start_city][1] # city_d is the same as g(s) in this case
    for ind, succ_city in enumerate(road_hash_Map[start_city]):
        if succ_city in closed and closed[succ_city][1] <= city_d + 1:
            continue
        closed[succ_city] = [start_city, city_d + 1] # Marking visited cities to avoid infinite-loops

        hs = 0
        if succ_city in city_pos_map: # defining h(s): heuristic function
            hs = abs(city_pos_map[succ_city][0] - city_pos_map[end_city][0]) +\
                 abs(city_pos_map[succ_city][1] - city_pos_map[end_city][1])
        heapq.heappush(fringe, (city_d + 1 + hs * 25, succ_city))
    while len(fringe) > 0:
        city = heapq.heappop(fringe)
        city = city[1]
        path.append(city)
        if (city == end_city): return
        return astar_search(city, end_city, road_hash_Map, cost_function, closed, path, city_pos_map)

    return



def main_search(start_city, end_city, road_hash_Map, routing_algorithm, cost_function, city_pos_map):
    if routing_algorithm in ["dfs", "bfs"]: return blind_search(start_city, end_city, road_hash_Map, routing_algorithm, cost_function)
    elif routing_algorithm == "ids":
        path = []
        d = 0
        while path == []:
            path, closed = blind_search(start_city, end_city, road_hash_Map, "dfs", cost_function, d)
            d += 1
        return path, closed
    elif routing_algorithm == "astar":
        closed = {}
        closed[start_city] = ["-1", 0]
        path = []
        astar_search(start_city, end_city, road_hash_Map, cost_function, closed, path, city_pos_map)
        return path, closed
    return [], {}
if __name__ == "__main__":
    start_city, end_city, routing_algorithm, cost_function = "", "", "", ""
    try:
        args = iter(argv)
        next(args)
        start_city = next(args)
        end_city = next(args)
        routing_algorithm = next(args)
        cost_function = next(args)
    except:
        print("NOT ENOUGH INPUTS!!!")

    road_segments = load_data("./road-segments.txt", " ")
    city_gps = load_data("./city-gps.txt", " ")
    city_pos_map = {}
    for city, lat, lon in city_gps:
        city_pos_map[city] = [lat, lon]
    road_hash_Map = {}
    for highway in road_segments:
        key = highway[0]#.split(',')[0]
        value = highway[1]#.split(',')[0]
        if key not in road_hash_Map: road_hash_Map[key] = [value]
        else: road_hash_Map[key].append(value)
        if value not in road_hash_Map: road_hash_Map[value] = [key]
        else: road_hash_Map[value].append(key)
    path, closed = main_search(start_city, end_city, road_hash_Map, routing_algorithm, cost_function, city_pos_map)
    best_path = draw_plot(path, closed, city_pos_map, routing_algorithm, cost_function)
    print("Path length: ", closed[path[-1]][1] + 1)
    print("\t".join(best_path))