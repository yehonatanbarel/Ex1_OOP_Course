import pandas as pd
import numpy as np
import random
import json
from AllInOne import building, elevator, elevator_call
import sys


# this func will get the json file and the CSV file as an input and will work on it
def Ex1(json_file, input_csv, output_csv):
    df = pd.read_csv(input_csv, header=None)
    pd.options.mode.chained_assignment = None
    b1 = building(json_file)

    if b1.numOfElevator == 1:
        for j in range(len(df)):
            df.iat[j, 5] = 0
    # if(building.numOfElevator<1) throw exception
    if b1.numOfElevator < 1:
        raise TypeError('NO ELEVATOR IN BUILDING')
    donelist = []
    index = 0
    speed_avg = 0

    fastspeed = 0
    fastlist = []
    bigfloor = abs(b1.maxFloor - b1.minFloor) * 0.75   #for case that the elevator have to reach 3/4 of the building -> send a fast elevator.

    """find the max speed of all elevators ,and save in a list all the "fast elevators".   """
    for i in range(b1.numOfElevator):
        elev = elevator(b1.elevators, i)
        speed_avg = speed_avg + elev.speed   #insert the avarage speed to a variable
        if (fastspeed < elev.speed):
            fastspeed = elev.speed
    for i in range(b1.numOfElevator):
        elev1 = elevator(b1.elevators, i)
        if (fastspeed == elev1.speed):
            fastlist.append(i)
    speed_avg = speed_avg / b1.numOfElevator
    min = 10000000000000  # sys.maxint

    """time_to_run - calculate how many times doing this algorithm """
    num_of_elev = b1.numOfElevator
    num_of_calls = len(df)
    sum_elev_calls = num_of_elev * num_of_calls
    if sum_elev_calls < 500:
        time_to_run = 300
    elif sum_elev_calls < 1000:
        time_to_run = 50
    else:
        time_to_run = 20

    for i in range(time_to_run):
        # we need to init the variable inside this for loop because we want
        # them to start from the begging every time
        sum = 0
        floor = 0
        floors = 0
        elevtime = 0
        wait = 0
        for j in range(len(df)):
            x = random.randint(0, b1.numOfElevator - 1)
            # decide which elev will get this call
            #if there is more than 5 elevators, we decide to send faster elevators.
            if (b1.numOfElevator > 5):
                elev1 = elevator(b1.elevators, x)
                if (elev1.speed < speed_avg):
                    x = random.randint(0, b1.numOfElevator - 1)
                    elev2 = elevator(b1.elevators, x)
                    if (elev2.speed < speed_avg):
                        x = random.randint(0, b1.numOfElevator - 1)
            df.iat[j, 5] = x

        parm = 0
        #for case that the elevator have to reach 3/4 of the building -> send a fast elevator from the list.

        if (len(fastlist) > 1):
            for s in range(len(df)):
                if (abs(df.iloc[s, 2] - df.iloc[s, 3]) > bigfloor):
                    df.iat[s, 5] = fastlist[parm]
                    parm = parm + 1
                    if (parm >= (len(fastlist))):
                        parm = 0


        """We run in a loop on the elevators, and in this loop we start another loop that goes over every call.
            In every call we check if the elevator assignment is the same index of the elevator in the outside loop. 
            If this is it, we sum the floors that he has to reach in the call between src to dest.
            and when the insider loop ends , it starts a new loop that sum of the floors that 
            he has to reach in the call between dest to the next src .
            In every iteration it will calculate the estimated time of all the floors that every elevator will reach 
            (it considers the speed , stop time, start time , open time , close time )."""

        stops = len(df) * 2 - 1
        for t in range(b1.numOfElevator - 1):
            elev = elevator(b1.elevators, t)
            for s in range(len(df)):
                if df.iat[s, 5] == t:
                    floors = floors + abs(df.iloc[s, 2] - df.iloc[s, 3])
            for k in range(
                    len(df) - 1):
                if df.iat[k, 5] == t:
                    floors = floors + abs(df.iat[k + 1, 2] - df.iat[k, 3])

            sum = sum + floors / elev.speed + stops * (elev.closeTime + elev.openTime + elev.stopTime + elev.startTime)

            """We run in a loop on the calls , and in every call we take the "call time" 
           ,"call time" of the next call , time that takes the elevator to reach the first call.
            Now it remains for us to test whether the difference between the first call time and the second call time. 
            And will the time it takes for the elevator to make the first call be greater than the remainder? 
            If so, then we have a deviation = delay of the elevator.
            if|callTime1-callTime2| < time it takes for the elevator to make the call
            So we do that for all the list of calls , and this is one of the main checks that we are doing."""

        for r in range(len(df) - 1):
            time = abs(df.iat[r, 1] - df.iat[r + 1, 1])
            floor = abs(df.iat[r, 2] - df.iat[r, 3])
            ind = df.iat[r, 5]
            elev = elevator(b1.elevators, ind)
            closeTime = elev.closeTime
            openTime = elev.openTime
            stopTime = elev.stopTime
            startTime = elev.startTime
            speed = elev.speed
            elevtime = elevtime + floor / speed + (closeTime + openTime + stopTime + startTime)
            if elevtime > time:
                wait = elevtime - time

        #insert the two parameters to variable that represents the estimated time.
        total_time = wait + sum
        donelist.append(list(df.iloc[:, 5]))   #saving the list of the elevators is an array.
        if min > (total_time):
            min = total_time
            index = i
    for i in range(len(df)):
        df.iat[i, 5] = donelist[index][i]
    export_csv = df.to_csv(r'out.csv', index=False, header=None)

    return export_csv



# ==============================================================

if __name__ == '__main__':
    Ex1(sys.argv[1], sys.argv[2], sys.argv[3])
