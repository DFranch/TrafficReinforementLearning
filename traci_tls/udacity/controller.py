# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys, os

import numpy as np
"""
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, merge
from keras.optimizers import Adam
"""
from env import FickDich
from gym import spaces

import os
import subprocess
import sys
import shutil
"""
from rl.agents import ContinuousDQNAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess
from rl.core import Processor
"""
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

from traci import simulation, trafficlights, simulationStep, close

step = 0
tl = trafficlights

reward_range = (-np.inf, np.inf)
observation_space = spaces.Box(low=0, high=1000, shape=(1, 19))

edges = []
TLSID = "0"

e = FickDich(12)
action_space = spaces.Discrete(2)
e.reset()

for i in range(1, 1000):

    arrived_vehicles_in_last_step = simulation.getArrivedNumber()
    departed_vehicles_in_last_step = simulation.getDepartedNumber()
    current_simulation_time_ms = simulation.getCurrentTime()

    result = e.step(action_space.sample())

    phase = trafficlights.getPhase(TLSID)

    lanes = trafficlights.getControlledLanes(TLSID)

    step += 1

    print(result)
e.close()
