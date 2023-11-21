from datetime import datetime, timedelta
from collections import deque, defaultdict
import pandas as pd
import json as js
import time
import heapq
from functions import *
import queue
import math

driversdata = pd.read_csv("drivers.csv")
passengersdata = pd.read_csv("passengers.csv")
edge_data = pd.read_csv("edges.csv")

driverstuples = createdriverstuple(driversdata)
passengerstuples = createpassengerstuple(passengersdata)

global edgetuples
edgetuples = getEdgeInfo(edge_data)

n = open("node_data.json")
node_data = js.load(n)

global nodetuples
nodetuples = getNodeInfo(node_data)


# defining what our graph looks like
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]

    def addEdgeToAdjMatrix(self, u, v, w):
        # where w = the list with avg times given date/time
        self.graph[u][v] = w

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
        # Initialize minimum distance for next node
        min = 1e7

        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index


def t1():
    # create maxheap for passengers (organized by wait time)
    heapq._heapify_max(passengerstuples)

    # initializing FIFO queue for drivers
    dq = queue.Queue(maxsize=len(driverstuples))
    for d in driverstuples:
        # put each driver in the queue
        dq.put(d)

    # Create match
    for passenger in passengerstuples:
        # pop out the firt elem aka first driver
        driver_to_match = dq.get()
        # and put it back into the back of the queue
        dq.put(driver_to_match)

        # Find match
        next_passenger = heapq._heappop_max(passengerstuples)
        match = (next_passenger[1], driver_to_match[1])
        # print(next_passenger)
        # print(driver_to_match)
        print(match)
    return


def t2():
    # dictionary with driver-passanger pairs as keys and distances as values
    dpDistances = defaultdict(list)
    calculatingDistances(dpDistances)

    # print(dpDistances.get(passengerstuples[1]))

    heapq._heapify_max(passengerstuples)

    # initializing FIFO queue for drivers
    dq = deque()
    for d in driverstuples:
        # put each driver in the queue
        dq.append(d)

    # Create match
    for passenger in passengerstuples:
        if not passengerstuples:
            return
        if not dq:
            return

        next_passenger = heapq._heappop_max(passengerstuples)

        driver_to_match = min(dpDistances.get(next_passenger), key=lambda x: x[1])
        driver_to_match = driver_to_match[0]

        # if this is the closet match
        if dq[0] == driver_to_match:
            # pop out the firt elem aka first driver
            dq.popleft()
            # and put it back into the back of the queue
            # dq.push(driver_to_match)
        else:
            # Find new match
            if driver_to_match not in dq:
                driver_to_match = dq.popleft()
            else:
                dq.remove(driver_to_match)

        # driver_to_match
        match = (driver_to_match, next_passenger)

        # print(next_passenger)
        # print(driver_to_match)
        # print(match)
    return match


# returns w_list with two nested arrays: 1st one
# is a list of estimated time to travel on a certain road/edge
# on a certain weekday and hour.
# 2nd nested array is same idea but on a certain weekend.
def buildEdgeWeights(t):
    w_list = []
    wkday_avg_times = []
    wkend_avg_times = []

    # print(t)
    # print("t[3] aka each wkday speed: ", str(t[3]))
    # print("length of wkday speed tuple in t: ", str(len(t[3])))

    for wkday_speed in t[3]:
        wkday_avg_times.append(
            t[2] / wkday_speed
        )  # length of road/avg speed on that given hour

    for wkend_speed in t[4]:
        wkend_avg_times.append(
            t[2] / wkend_speed
        )  # length of road/avg speed on that given hour

    w_list.append(wkday_avg_times)
    w_list.append(wkend_avg_times)
    return w_list  # 1st element: wkday_avg_times, 2nd element: wkend_avg_times


def buildGraph(i, edgetuples, ind_node_dict):
    # newset = set()
    # for t in edgetuples:
    #     newset.add(t[0])
    #     newset.add(t[1])

    # scrapping the code above because it makes the matrix way too big.
    # memory cant handle it!!!

    network = Graph(i)  # graph represented by i x i matrix

    for t in edgetuples:
        w_list = buildEdgeWeights(t)
        network.addEdgeToAdjMatrix(
            ind_node_dict.get(t[0]), ind_node_dict.get(t[1]), w_list
        )
    return network


def findClosestNode(driver_coords, nodes_arr):
    min = float("inf")
    ret = [nodes_arr[0]]
    for n in nodes_arr:
        if math.dist(n, driver_coords) < min:
            min = math.dist(n, driver_coords)
            ret[0] = n
    return ret[0]


def convertDecimalHours(n):
    minutes = n * 60
    seconds = n * 3600

    return (minutes, seconds)


def clock(curr_dt, estimated_time):
    ms_tup = convertDecimalHours(estimated_time)

    # convert float to int because timedelta only accepts int values
    minutes = round(ms_tup[0])
    seconds = round(ms_tup[1])

    # add minutes to datetime
    time_change = timedelta(minutes=minutes, seconds=seconds)
    new_time = curr_dt + time_change
    return new_time


def getCorrectWeight(curr_dt, network, current_node, k):
    # check if current day is a weekday or wkend
    day_type = 0
    if curr_dt.weekday() >= 5:
        day_type = 1

    # get the hour from current_datetime
    hour = curr_dt.hour

    return network[current_node][k][day_type][hour]


# returns estimated time, in minutes.
def t3():
    # keys = node ids, values = index in adj matrix
    ind_node_dict = dict()
    i = 0
    for nt in nodetuples:
        ind_node_dict[int(nt[0])] = i
        i += 1

    network = buildGraph(i, edgetuples, ind_node_dict)

    # get output of t2 (the match tuple? i'm assuming we're
    # returning that from t2 but idk)
    match = t2()
    # print(match)

    # we just need the chosen driver from t2()
    driver_coords = (match[0][1][1], match[0][1][2])
    # print(driver_coords)

    passenger_coords = (match[1][1][3], match[1][1][4])

    # key = node's coordinate; value = node id
    nodes_dict = dict()
    nodes_arr = []
    for node in nodetuples:
        nodes_dict[(node[1], node[2])] = node[0]
        nodes_arr.append((node[1], node[2]))
    closest_vertex_to_driver = findClosestNode(driver_coords, nodes_arr)
    closest_vertex_to_pass = findClosestNode(passenger_coords, nodes_arr)

    # get node id of node to start traversal on
    s = nodes_dict.get(closest_vertex_to_driver)

    # get index of that node in adj matrix
    s_ind = ind_node_dict.get(nodes_dict.get(closest_vertex_to_driver))

    # get node id of node to finish traversal on
    t = nodes_dict.get(closest_vertex_to_pass)

    # get index of that node in adj matrix
    t_ind = ind_node_dict.get(nodes_dict.get(closest_vertex_to_pass))

    num_nodes = i + 1

    # Initialize distance and visited arrays
    distances = [float("inf")] * num_nodes
    visited = []
    estimated_time = sum(distances)

    # Set distance at starting node to 0 and add to visited list
    # serves as our priority queue
    distances[s_ind] = 0

    curr_dt = datetime.strptime(match[0][1][0], "%m/%d/%Y %H:%M:%S")

    # Loop through all nodes to find shortest path to each node
    for j in range(num_nodes):
        # Find minimum distance node that has not been visited yet
        current_node = minDistance(distances, visited)

        # Add current_node to list of visited nodes
        visited.append(current_node)

        # Loop through all neighbors of current_node
        for k in range(num_nodes):
            # Check if there is an edge from current_node to neighbor
            if network.graph[current_node][k] != 0:
                # get the correct edge weight for this edge
                weight = getCorrectWeight(curr_dt, network, current_node, k)
                # Calculate the distance from start_node to neighbor,
                # passing through current_node
                new_distance = distances[current_node] + weight

                # Update the distance if it is less than previous recorded value
                if new_distance < distances[k]:
                    distances[k] = new_distance
                    # since we updated distances, we need to update
                    clock(curr_dt, estimated_time)
    return estimated_time


# finds node with the smallest distance
# that has not been visited yet
def minDistance(distances, visited):
    # Initialize minimum distance for next node
    min_val = float("inf")
    min_index = -1

    # Loop through all nodes to find minimum distance
    for i in range(len(distances)):
        if distances[i] < min_val and i not in visited:
            min_val = distances[i]
            min_index = i

    return min_index


# def convertTwelveHr(military_time):
#    # Parse the military time string into a datetime object
#    just_time = military_time.split()
#    dt = datetime.strptime(just_time, '%H:%M:%S')
#    # Format the datetime object into a regular time string
#    return dt.strftime('%I:%M:%S %p')

# def t3():
#     dpTravelTimes = defaultdict(list)

#     heapq._heapify_max(passengerstuples)

#     # initializing FIFO queue for drivers
#     dq = deque()
#     for d in driverstuples:
#         # put each driver in the queue
#         dq.append(d)

#     # Create match
#     for passenger in passengerstuples:
#         if not passengerstuples:
#             return
#         if not dq:
#             return

#         next_passenger = heapq._heappop_max(passengerstuples)

#         driver_to_match = min(dpTravelTimes.get(next_passenger), key=lambda x: x[1])
#         driver_to_match = driver_to_match[0]

#         # if this is the closet match
#         if dq[0] == driver_to_match:
#             # pop out the firt elem aka first driver
#             dq.popleft()
#             # and put it back into the back of the queue
#             # dq.push(driver_to_match)
#         else:
#             # Find new match
#             if driver_to_match not in dq:
#                 driver_to_match = dq.popleft()
#             else:
#                 dq.remove(driver_to_match)

#         # driver_to_match
#         match = (driver_to_match, next_passenger)

#         # print(next_passenger)
#         # print(driver_to_match)
#         # print(match)
#     return


def main():
    # driver_coords = (9, 3)
    # nodes_arr = [(9,3), (9, 3.5), (4, 2)]
    # print("closest Coordinaates: ")
    # print(findClosestNode(driver_coords, nodes_arr))
    # print(edgetuples)
    # print(len(edgetuples[0]))
    n = 0.0138432
    print(convertHours(n))
    # t3()


if __name__ == "__main__":
    main()
