from datetime import datetime
import pandas as pd

driversdata=pd.read_csv('drivers.csv')


def createdriverstuple(driversdata):
    listdrivers=[]
    datetimes=driversdata["Date/Time"]

    for i in range(len(datetimes)):
        wait=findelapsedtime(datetimes[i])
        tupledriver=(wait,(driversdata["Date/Time"][i],driversdata["Source Lat"][i],driversdata["Source Lon"][i]))
        listdrivers.append(tupledriver)
    
    return listdrivers



def findelapsedtime(requesttime):
    currenttime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    curr = datetime.strptime(currenttime, "%m/%d/%Y %H:%M:%S")
    req = datetime.strptime(requesttime, "%m/%d/%Y %H:%M:%S")
    elapsedtime = req - curr
    return elapsedtime.total_seconds()



print(driversdata["Date/Time"][0])
print(findelapsedtime(driversdata['Date/Time'][0]))
print(createdriverstuple(driversdata))





