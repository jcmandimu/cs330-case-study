from datetime import datetime
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
    return


def buildEdgeWeights(t):
    w_list = []
    wkday_avg_times = []
    wkend_avg_times = []
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
    return w_list


def buildGraph(edgetuples):  # will have to run this several times
    newset = set()
    for t in edgetuples:
        newset.add(t[0])  # 0th element of each tuple is one vertex of tht edge
        newset.add(t[1])  # 1st element of each tuple is other vertex of tht edge

    network = Graph(max(newset))

    for t in edgetuples:
        w_list = buildEdgeWeights(t)

    network.addEdgeToAdjMatrix(t[0], t[1], w_list)
    return network


# returns s: starting vertex for t3()/Dijkstra's
def findClosestNode(driver_coords, nodes_arr):
    # Base case: if the list is empty, return None
    if not nodes_arr:
        return None

    if len(nodes_arr) == 1:
        return nodes_arr[0]

    # Divide the list into two halves
    mid = len(nodes_arr) // 2
    left = nodes_arr[:mid]
    right = nodes_arr[mid:]

    # Recursively find the closest coordinate in the left and right halves
    closest_left = findClosestNode(driver_coords, left)
    closest_right = findClosestNode(driver_coords, right)

    # If the closest coordinate is in the left half, return it
    if not closest_right or math.dist(closest_left, driver_coords) < math.dist(
        closest_right, driver_coords
    ):
        return closest_left

    # If the closest coordinate is in the right half, return it
    return closest_right


def t3(nodetuples, edgetuples):
    # we want all the vertices
    network = buildGraph(edgetuples)

    # get output of t2 (the match tuple? i'm assuming we're
    # returning that from t2 but idk)
    match = t2()

    # we just need the chosen driver from t2()
    driver_coords = (match[0][1][1], match[0][1][2])

    # key = node's coordinate; value = node id
    nodes_dict = dict()
    nodes_arr = []
    for node in nodetuples:
        nodes_dict[(node[2], node[1])] = node[0]
        nodes_arr.append((node[2], node[1]))

    closest_vertex = findClosestNode(driver_coords, nodes_arr)
    s = nodes_dict.get(closest_vertex)


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
    # p = (9, 3)
    # d = [(1, 0), (9, 4), (4, 2)]
    # print(closestDriver(p, d))
    print(t2())
    # buildGraph(edgetuples)


if __name__ == "__main__":
    main()
