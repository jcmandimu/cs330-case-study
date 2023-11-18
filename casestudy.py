from datetime import datetime
from collections import deque
import pandas as pd
import json as js
import time
import heapq
from functions import *
import queue
import math


driversdata=pd.read_csv('drivers.csv')
passengersdata=pd.read_csv('passengers.csv')

driverstuples=createdriverstuple(driversdata)
passengerstuples=createpassengerstuple(passengersdata)



def t1():
    #create maxheap for passengers (organized by wait time)
    heapq._heapify_max(passengerstuples)

    #initializing FIFO queue for drivers
    dq=queue.Queue(maxsize=len(driverstuples))
    for d in driverstuples:
        #put each driver in the queue
        dq.put(d)
        
    #Create match
    for passenger in passengerstuples:
         #pop out the firt elem aka first driver
        driver_to_match=dq.get()
        #and put it back into the back of the queue
        dq.put(driver_to_match)

        #Find match
        next_passenger=heapq.heappop(passengerstuples)
        match=(next_passenger[1],driver_to_match[1])
        # print(next_passenger)    
        # print(driver_to_match)
        print(match)
    return match
    
# t1()
 
def t2():
    # dictionary with driver-passanger pairs as keys and distances as values
    dpDistances = defaultdict(list)
    calculatingdpDistances(dpDistances)

    # print(dpDistances.get(passengerstuples[1]))

    heapq._heapify_max(passengerstuples)

    #initializing FIFO queue for drivers
    dq=queue.Queue(maxsize=len(driverstuples))
    for d in driverstuples:
        #put each driver in the queue
        dq.put(d)
    
    #Create match
    for passenger in passengerstuples:
        
        next_passenger=heapq.heappop(passengerstuples)
        driver_to_match = min(dpDistances.get(next_passenger), key=lambda x: x[1])


        #if this is the closet match
        if(dq.get() == driver_to_match[0]):
            #pop out the firt elem aka first driver
            driver_to_match=dq.get()
            #and put it back into the back of the queue
            # dq.put(driver_to_match)
        else:
        #Find match
            driver_to_match=min(dpDistances.get(next_passenger), key=lambda x: x[1])
            dq.get(driver_to_match[0])
            # dq.put(driver_to_match[0])
            driver_to_match = driver_to_match[0]

        
        # driver_to_match 
        match=(driver_to_match, next_passenger)


        # print(next_passenger)    
        # print(driver_to_match)
        print(match)
    return match
    


t2()
