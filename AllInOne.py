import json

import pandas as pd


class building:

    # this will open the json file and get min / max floor , the data for the elevator of the
    # building and the number of elevator for this building
    def __init__(self, file_build):
        with open(file_build, "r") as p:
            data = json.load(p)
            self.minFloor = data['_minFloor']
            self.maxFloor = data['_maxFloor']
            self.elevators = data['_elevators']
            self.numOfElevator = len(data['_elevators'])


class elevator:
    # notice that this 'data' below that is given as parameter to 'def' is a dictionary
    # ( data['_elevators'] is a list that contains a dictionary so we cant reach a value by  data['_id']
    # we need to do data['_elevators'][0]['_id'] )
    def __init__(self, data, index_elev):
        self.index_elev = index_elev
        self.id = data[index_elev]['_id']
        self.speed = data[index_elev]['_speed']
        self.minFloor = data[index_elev]['_minFloor']
        self.maxFloor = data[index_elev]['_maxFloor']
        self.closeTime = data[index_elev]['_closeTime']
        self.openTime = data[index_elev]['_openTime']
        self.startTime = data[index_elev]['_startTime']
        self.stopTime = data[index_elev]['_stopTime']


class elevator_call:
    def __init__(self, call):
        df = pd.read_csv(call, header=None)
        # This will get the whole column itself for each
        # 'time' - 1 / 'src' - 2 / 'dest' - 3 / 'allocatedTo' - 5
        self.getTime = df.iloc[:, 1]
        self.src = df.iloc[:, 2]
        self.dest = df.iloc[:, 3]
        self.allocatedTo = df.iloc[:, 5]


