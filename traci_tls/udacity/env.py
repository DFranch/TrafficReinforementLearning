from __future__ import division
import numpy as np
from gym.utils import seeding
import sys
import os
from gym import spaces


try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  # noqa
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


import traci

class FickDich(object):
    """Ubuntu Config"""
    # sys.path.append('/usr/share/sumo/tools')

    sumoBinary = checkBinary('sumo-gui')
    sumoCmd = [sumoBinary, "-c", "../data/cross.sumocfg"]

    reward_range = (-np.inf, np.inf)
    action_space = None
    observation_space = spaces.Box(low=0,high=1000, shape=(1,19))

    edges = []


    def __init__(self):
        self.lanes = 12

        self.action_space = spaces.Discrete(2)
        self.reward_range = (-np.inf, np.inf)
        self.observation_space = spaces.Box(low=0, high=1000, shape=(1, 19))
        self.TLSID = "0"


    def step(self, action):
        traci.simulationStep()
        # read global info

        arrived_vehicles_in_last_step = traci.simulation.getArrivedNumber()
        departed_vehicles_in_last_step = traci.simulation.getDepartedNumber()
        current_simulation_time_ms = traci.simulation.getCurrentTime()
        vehicles_started_to_teleport = traci.simulation.getStartingTeleportNumber()
        vehicles_ended_teleport = traci.simulation.getEndingTeleportNumber()
        vehicles_still_expected = traci.simulation.getMinExpectedNumber()
        action = self.convert_sample_to_phase(action)
#        print("   ----- State: {}".format(action))

        #traci.trafficlights.setRedYellowGreenState('0', action)


        observation = [arrived_vehicles_in_last_step, departed_vehicles_in_last_step,
                       current_simulation_time_ms, vehicles_started_to_teleport,
                       vehicles_ended_teleport, vehicles_still_expected]

        reward = 0
        avg_edge_values = np.zeros(1)
        for e_id in self.edges:
            edge_values = [
                traci.edge.getCO2Emission(e_id),
            ]
            avg_edge_values = np.add(avg_edge_values, edge_values)

        print(avg_edge_values)
        observation = [avg_edge_values]

        reward += -avg_edge_values

        done = False
        info = reward

        return observation, reward, done, info



    def reset(self):
        traci.start(self.sumoCmd)
        lanes = traci.trafficlights.getControlledLanes(self.TLSID)
        for lane in lanes:
            self.edges.append(traci.lane.getEdgeID(lane))

        return np.zeros(19)

    def render(self, mode='human', close=False):
        return

    def close(self):
        traci.close()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def configure(self, *args, **kwargs):
        raise NotImplementedError()

    def __del__(self):
        self.close()

    def __str__(self):
        return '<{} instance>'.format(type(self).__name__)

    def convert_sample_to_phase(self, sample):
        if sample == 1:
            return 'rgrg'
        else:
            return 'grgr'