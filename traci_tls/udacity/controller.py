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
from env import FickDich

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


e = FickDich(12)
print(e.action_space)
e.reset()
TLSID = "0"
for i in range(1,1000):

    current_simulation_time_ms = simulation.getCurrentTime()

    now = current_simulation_time_ms/1000
    prev_time = now / 1000

    if ((now - prev_time) > 1000):
        result = e.step('GrGr')
    else:
        result = e.step('rGrG')

    arrived_vehicles_in_last_step = simulation.getArrivedNumber()
    departed_vehicles_in_last_step = simulation.getDepartedNumber()

    phase = trafficlights.getPhase(TLSID)

    lanes = trafficlights.getControlledLanes(TLSID)

    print(phase)
    #if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
    #    traci.trafficlights.setRedYellowGreenState("0", "GrGr")
    step += 1

    #print(result)
e.close()