from datetime import datetime
import pandas as pd
import json as js
import time
import heapq
from functions import *


driversdata=pd.read_csv('drivers.csv', nrows=5)
passengersdata=pd.read_csv('passengers.csv', nrows=5)

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

# print(driverstuples)
print(passengerstuples)

#create minheap

heapq.heapify(driverstuples)
heapq._heapify_max(passengerstuples)

# print(heapq.heappop(driverstuples))
print(heapq.heappop(passengerstuples))



