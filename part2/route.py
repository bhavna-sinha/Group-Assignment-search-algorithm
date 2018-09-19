#!/bin/python
import pandas as pd
import numpy as np
from sys import argv, exit
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker

def load_data(data_path, seprt):
    unarng_data = pd.read_table(data_path, sep=seprt, header=None)
    unarng_data = unarng_data.values
    return unarng_data

def draw_plot(path, city_pos_map):
    blit = False
    fig_m, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5 * 3, 5 * 3))
    plt.rcParams.update({'font.size': 6})
    fig_m.tight_layout(rect=[0, 0, 0.9, 1])
    # fig_m.subplots_adjust(hspace=.1)
    ax0 = plt.subplot(111)#, sharex=ax0)
    #plt.margins(x=0)
    ax0.set_xlim(np.min(city_gps[:, 1]), np.max(city_gps[:, 1]))
    ax0.set_ylim(np.min(city_gps[:, 2]), np.max(city_gps[:, 2]))
    ax0.xaxis.set_major_locator(ticker.LinearLocator(20))
    ax0.xaxis.set_minor_locator(ticker.LinearLocator(20))
    ax0.xaxis.grid(True, linestyle='--', which='major', color='black', alpha=1.0)
    ax0.yaxis.grid(True, linestyle='--', which='major', color='black', alpha=1.0)
    ax0.set_ylabel('longitude')
    ax0.set_xlabel('latitude')
    ax0.set_title('Map of cities')
    # for key in city_pos_map.keys():
    #     ax0.text(city_pos_map[key][0], city_pos_map[key][1], key.split(',')[0], ha='center')

    if blit: fig_m.canvas.draw()

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
    for key in path[1:-1]:
        if key in city_pos_map:
            ax0.text(city_pos_map[key][0], city_pos_map[key][1], key.split(',')[0], ha='center', color='blue')
        else:
            ax0.text(40, -100, city.split(',')[0], ha='center', color='blue')
        if blit:
            fig_m.canvas.restore_region(axbackground)
            fig_m.canvas.blit(ax0.bbox)
        plt.pause(1e-10)



    #plt.savefig("%sTF_Sample" % data_path)#, bbox_inches='tight')
    plt.show()

def blind_search(start_city, end_city, closed, road_hash_Map, routing_algorithm, cost_function):
    path = []
    pop_pos = -1 if (routing_algorithm == "dfs") else 0
    fringe = [start_city]
    closed[start_city] = 1
    while (len(fringe) > 0):
        city = fringe.pop(pop_pos)
        path.append(city)
        if (city == end_city): return path
        fringe_updated = False
        for succ_city in road_hash_Map[city]:
            if succ_city not in closed: closed[succ_city] = 1 # Marking visited cities to avoid infinite-loops
            else: continue
            fringe_updated = True
            fringe.append(succ_city)
        if not fringe_updated: path.pop() # Remove a city from our path which is dead-end and just has visited successors

    return ["NOT FOUND!!!"]

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
    closed = {}
    path = blind_search(start_city, end_city, closed, road_hash_Map, routing_algorithm, cost_function)
    draw_plot(path, city_pos_map)
    print(",".join(path))