from datetime import datetime
import pandas as pd
import json as js
import time
import heapq
import math
from collections import defaultdict


driversdata = pd.read_csv("drivers.csv", nrows = 1)
passengersdata = pd.read_csv("passengers.csv")
# edge_data = pd.read_csv("edges.csv")


n = open("node_data.json")
node_data = js.load(n)


def getNodeInfo(node_data):
    list_nodes = []
    for n_id in node_data:
        list_nodes.append((n_id, node_data[n_id]["lat"], node_data[n_id]["lon"]))
    return list_nodes


# reading from edges.csv
def getEdgeInfo(edge_data):
    list_edges = []
    for i, row in edge_data.iterrows():
        # making part of edge tuple where you just get start_id, end_id, and length
        tuple_edge = (
            row["start_id"].astype(int),  # start_id
            row["end_id"].astype(int),  # end_id
            row["length"],  # length
            # so sorry abt how silly and long this is
            (
                row["weekday_0"],
                row["weekday_1"],
                row["weekday_2"],
                row["weekday_3"],
                row["weekday_4"],
                row["weekday_5"],
                row["weekday_6"],
                row["weekday_7"],
                row["weekday_8"],
                row["weekday_9"],
                row["weekday_10"],
                row["weekday_11"],
                row["weekday_12"],
                row["weekday_13"],
                row["weekday_14"],
                row["weekday_15"],
                row["weekday_16"],
                row["weekday_17"],
                row["weekday_18"],
                row["weekday_19"],
                row["weekday_20"],
                row["weekday_21"],
                row["weekday_22"],
                row["weekday_23"],
            ),
            (
                row["weekend_0"],
                row["weekend_1"],
                row["weekend_2"],
                row["weekend_3"],
                row["weekend_4"],
                row["weekend_5"],
                row["weekend_6"],
                row["weekend_7"],
                row["weekend_8"],
                row["weekend_9"],
                row["weekend_10"],
                row["weekend_11"],
                row["weekend_12"],
                row["weekend_13"],
                row["weekend_14"],
                row["weekend_15"],
                row["weekend_16"],
                row["weekend_17"],
                row["weekend_18"],
                row["weekend_19"],
                row["weekend_20"],
                row["weekend_21"],
                row["weekend_22"],
                row["weekend_23"],
            ),
        )
        list_edges.append(tuple_edge)
    # print(list_edges)
    return list_edges
    # debugging for weekday info:
    # print("tuple w/ JUST weekdays: ")
    # print(tuple(row["weekday_0":"weekday_23"]))
    # print(str(len(tuple(row["weekday_0":"weekday_23"]))))

    # tuple_edge += tuple(row["weekday_0":"weekday_23"])

    # debugging for weekday info:
    # print("tuple w/ JUST weekends: ")
    # print(tuple(row["weekend_0":"weekend_23"]))
    # print(str(len(tuple(row["weekend_0":"weekend_23"]))))

    # tuple_edge += tuple(row["weekend_0":"weekend_23"])
    # debugging for weekday info:
    # print("\n length of tuple: ")
    # print(str(len(tuple_edge))) #shoud be first three elements + two nested tuples

    # print("\n num of rows: ")
    # print(str(len(tuple_edge)-2 + len(tuple_edge[3]) + len(tuple_edge[4]))) #s


# t1 functions
def createpassengerstuple(passengersdata):
    listpassengers = []
    datetimes = passengersdata["Date/Time"]

    for i in range(len(datetimes)):
        wait = abs(findelapsedtime(datetimes[i]))
        tuplepassenger = (
            wait,
            (
                passengersdata["Date/Time"][i],
                passengersdata["Source Lat"][i],
                passengersdata["Source Lon"][i],
                passengersdata["Dest Lat"][i],
                passengersdata["Dest Lon"][i],
            ),
        )
        listpassengers.append(tuplepassenger)

    return listpassengers


def createdriverstuple(driversdata):
    listdrivers = []
    datetimes = driversdata["Date/Time"]

    for i in range(len(datetimes)):
        wait = abs(findelapsedtime(datetimes[i]))
        tupledriver = (
            wait,
            (
                driversdata["Date/Time"][i],
                driversdata["Source Lat"][i],
                driversdata["Source Lon"][i],
            ),
        )
        listdrivers.append(tupledriver)
    return listdrivers


def findelapsedtime(requesttime):
    currenttime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    curr = datetime.strptime(currenttime, "%m/%d/%Y %H:%M:%S")
    req = datetime.strptime(requesttime, "%m/%d/%Y %H:%M:%S")
    elapsedtime = req - curr

    return elapsedtime.total_seconds()


driverstuples = createdriverstuple(driversdata)
passengerstuples = createpassengerstuple(passengersdata)

# print("The driver tuples: ")
# print(driverstuples)
# print(passengerstuples)


# t2 functiobs
def calculateDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))


def calculatingdpDistances(dists):
    for driver in driverstuples:
        for passenger in passengerstuples:
            distance = calculateDistance(
                driver[1][2], passenger[1][2], driver[1][1], passenger[1][1]
            )
            dists.update({(driver, passenger): distance})


# t2 functions
def calculateDistance(x1, x2, y1, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))


def calculatingDistances(dists):
    for driver in driverstuples:
        for passenger in passengerstuples:
            distance = calculateDistance(
                driver[1][1], passenger[1][1], driver[1][2], passenger[1][2]
            )
            dists[passenger].append((driver, distance))


# t3 functions
def calculatingTravelTimes(times):
    for driver in driverstuples:
        for passenger in passengerstuples:
            travelTime = calculateDistance(
                driver[1][1], passenger[1][1], driver[1][2], passenger[1][2]
            )
            times[passenger].append((driver, travelTime))


def findStart():
    return


def findEnd():
    return


def main():
    # # Opening JSON file
    # n = open("node_data.json")

    # # returns JSON object as a dictionary
    # node_data = js.load(n)
    # getNodeInfo(node_data)
    driversdata = pd.read_csv("drivers.csv", nrows = 1)
    print(createdriverstuple(driversdata))

#t4 functions
def astar(graph,start,end):
    return

#t5 functions
def calculatingDestDistances(dists):
    for driver in driverstuples:
        for passenger in passengerstuples:
            distance = calculateDistance(
                driver[1][1], passenger[1][3], driver[1][2], passenger[1][4]
            )
            dists[passenger].append((driver, distance))



if __name__ == "__main__":
    main()
