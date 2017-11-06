# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys, os

import numpy as np

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, merge
from keras.optimizers import Adam

import os
import subprocess
import sys
import shutil


from rl.agents import ContinuousDQNAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess
from rl.core import Processor

try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  # noqa
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

netconvertBinary = checkBinary('netconvert')
sumoBinary = checkBinary('sumo')
sumoCmd = [sumoBinary, "-c", "../data/hello.sumocfg"]


"""interesting functions:
    gui: screenshot()
        trackVehicle()
"""
import pandas as pd
from traci import simulation, trafficlights, simulationStep, close
import ast

retcode = subprocess.call(
    [sumoBinary, "-c", "../data/hello.sumocfg", "--no-step-log"], stdout=sys.stdout, stderr=sys.stderr)

step = 0
tl = trafficlights


def import_datasets():
    csv_dir = "..\\code\\"
    lust_file_name = "dataset-lust-tl-clusters.csv"
    df = pd.read_csv(csv_dir + lust_file_name)
    df['connections'] = df['connections'].map(lambda x: ast.literal_eval(x))
    return df


def extract_tl_ids(connection_list):
    tl_list = []
    for connection in connection_list:
        tl_list.append(connection[2])
    return tl_list


# lust= import_datasets()

# tls= extract_tl_ids(lust.iloc[0])
# print tls
# connections = dataset[5]==[from,to,tl,dir,state]
if True:
    TLSID = "0"
    while step < 1000:

        arrived_vehicles_in_last_step = simulation.getArrivedNumber()
        departed_vehicles_in_last_step = simulation.getDepartedNumber()
        current_simulation_time_ms = simulation.getCurrentTime()
        print(arrived_vehicles_in_last_step)
        phase = trafficlights.getPhase(TLSID)
        trafficlights.setRedYellowGreenState(TLSID, "grrrrrrrrrrr")

        lanes = trafficlights.getControlledLanes(TLSID)
        print(len(lanes))
        # for lane in lanes:
        #    print lane
        print(phase)
        # if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
        #   traci.trafficlights.setRedYellowGreenState("0", "GrGr")
        step += 1

    close()