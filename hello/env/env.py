from gym import Env
from gym import error, spaces, utils
from gym.utils import seeding
from scipy.misc import imread
from gym import spaces
from string import Template
import os, sys
import numpy as np
import math
import time

from __future__ import division
import numpy as np
import pandas as pd

import ast
import itertools
import sys
import os
from gym import spaces

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import traci.constants as tc


class TrafficEnv(Env):
    reward_range = (-np.inf, np.inf)
    action_space = None
    observation_space = spaces.Box(low=0, high=1000, shape=(1, 19))

    # spaces.Discrete(7) 0-6
    possible_actions = ['r', 'g', 'G', 'y', 'o', 'O', 'u']
    edges = []
    TLSID = "0"

    def __init__(self, lights, netfile, routefile, guifile, addfile, loops=[], lanes=[], exitloops=[],
                 tmpfile="tmp.rou.xml",
                 pngfile="tmp.png", mode="gui", detector="detector0", simulation_end=3600, sleep_between_restart=1):
        self.lanes = lanes
        space_init = []

        for i in range(0, lanes):
            space_init.append([0, 6])
        action_space = spaces.MultiDiscrete(space_init)

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _reward(self):
        return

    def _step(self, action):
        return

    def _observation(self):
        return

    def _reset(self):
        return

    def _render(self, mode='human', close=False):
        return
