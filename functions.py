from datetime import datetime
import pandas as pd
import json as js
import time
import heapq
import math
from collections import defaultdict



driversdata=pd.read_csv('drivers.csv')
passengersdata=pd.read_csv('passengers.csv')

#t1 functions
def createpassengerstuple(passengersdata):
    listpassengers=[]
    datetimes=passengersdata["Date/Time"]

    for i in range(len(datetimes)):
        wait=abs(findelapsedtime(datetimes[i]))
        tuplepassenger=(wait,(passengersdata["Date/Time"][i],passengersdata["Source Lat"][i],passengersdata["Source Lon"][i],passengersdata["Dest Lat"][i],passengersdata["Dest Lon"][i]))
        listpassengers.append(tuplepassenger)
    
    return listpassengers


def createdriverstuple(driversdata):
    listdrivers=[]
    datetimes=driversdata["Date/Time"]

    for i in range(len(datetimes)):
        wait=abs(findelapsedtime(datetimes[i]))
        tupledriver=(wait,(driversdata["Date/Time"][i],driversdata["Source Lat"][i],driversdata["Source Lon"][i]))
        listdrivers.append(tupledriver)
    
    return listdrivers



def findelapsedtime(requesttime):
    currenttime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    curr = datetime.strptime(currenttime, "%m/%d/%Y %H:%M:%S")
    req = datetime.strptime(requesttime, "%m/%d/%Y %H:%M:%S")
    elapsedtime = req - curr

    return elapsedtime.total_seconds()



driverstuples=createdriverstuple(driversdata)
passengerstuples=createpassengerstuple(passengersdata)

#t2 functions
def calculateDistance(x1,x2,y1,y2): 
    return math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

def calculatingdpDistances(dists):
    for driver in driverstuples:
        for passenger in passengerstuples:
            distance = calculateDistance(driver[1][1], passenger[1][1], driver[1][2], passenger[1][2])
            dists[passenger].append((driver,distance))

#print(driverstuples)
#print(passengerstuples)
