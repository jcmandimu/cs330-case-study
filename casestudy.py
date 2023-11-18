from datetime import datetime
import pandas as pd
import json as js
import time
import heapq
from functions import *
import queue


driversdata=pd.read_csv('drivers.csv')
passengersdata=pd.read_csv('passengers.csv')


def t1(driversdata,passengersdata):
    driverstuples=createdriverstuple(driversdata)
    passengerstuples=createpassengerstuple(passengersdata)

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
    

t1(driversdata,passengersdata)

