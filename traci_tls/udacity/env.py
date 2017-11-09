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
        avg_edge_values = np.zeros(13)
        for e_id in self.edges:
            print(traci.edge.getCO2Emission(e_id))
            edge_values = [
                traci.edge.getWaitingTime(e_id),
                traci.edge.getCO2Emission(e_id),
                traci.edge.getCOEmission(e_id),
                traci.edge.getHCEmission(e_id),
                traci.edge.getPMxEmission(e_id),
                traci.edge.getNOxEmission(e_id),
                traci.edge.getFuelConsumption(e_id),
                traci.edge.getLastStepMeanSpeed(e_id),
                traci.edge.getLastStepOccupancy(e_id),
                traci.edge.getLastStepLength(e_id),
                traci.edge.getTraveltime(e_id),
                traci.edge.getLastStepVehicleNumber(e_id),
                traci.edge.getLastStepHaltingNumber(e_id)
            ]
            #scale using the amount of vehicles
            if edge_values[11]>0:
                edge_values[7] /= edge_values[11]
                edge_values[1] /= edge_values[11]
                edge_values[0] /= edge_values[11]
            avg_edge_values = np.add(avg_edge_values, edge_values)


        avg_edge_values /= len(self.edges)

        observation.extend(avg_edge_values)

        waitingFactor = -avg_edge_values[0] / 100
        if waitingFactor == 0:
            waitingFactor += 1
        co2_factor = -avg_edge_values[1] / 3000
        fuel_factor = -avg_edge_values[7]
        green_factor=7*(action.count("g")+action.count("G"))/self.lanes
        yellow_factor=-0.5*action.count("y")/self.lanes
        red_factor=-2*action.count("r")/self.lanes

        reward += waitingFactor+co2_factor+fuel_factor+green_factor+yellow_factor+red_factor

        done = False
        info = {"waitingFactor": waitingFactor, "co2_factor":co2_factor,"fuel_factor":fuel_factor,
                "green_factor":green_factor,"yellow_factor":yellow_factor,"red_factor":red_factor,"total_reward":reward}

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