
'''
Author : Adil Moujahid
Email : adil.mouja@gmail.com
Description: Simulations of Schelling's seggregation model

You will need to set up pycharm to import matplotlib.
'''

import matplotlib.pyplot as plt
import itertools
import random
import copy
from Agent import Agent

class Stampede:
    def __init__(self, width, height, empty_ratio, n_iterations, weightDistribution):
        self.agents = []                                # array: holds all agents               # TODO: RIGHT NOW THIS IS AN ARRAY, USED TO BE STORED IN {}; DECIDE IF THIS IS A GOOD DECISION OR IF IT SHOULD BE {}
        self.width = width                              # int: width of the grid I think
        self.height = height                            # int: height of the grid I think
        self.empty_ratio = empty_ratio                  # float
        self.n_iterations = n_iterations                # int
        self.weightDistribution = weightDistribution    # dictionary: { "mean": , "sd":  }

    def populate(self):
        self.empty_spaces = []
        print("Populate ",  self.width ,  self.height)
        self.all_spaces = list(itertools.product(range(self.width), range(self.height)))
        print(self.all_spaces)
        random.shuffle(self.all_spaces)

        self.n_empty = int(self.empty_ratio * len(self.all_spaces))
        self.empty_spaces = self.all_spaces[:self.n_empty]

        self.remaining_spaces = self.all_spaces[self.n_empty:]

        print("n_empty: ", self.n_empty)
        print("empty_spaces: ", self.empty_spaces)
        print("remaining_space: ", self.remaining_spaces)

        self.agentsAppended = 0

        # create all agents and append them to self.agents
        while (len(self.empty_spaces) / len(self.all_spaces)) > self.empty_ratio:
            print("remaining_spaces ratio:", len(self.remaining_spaces) / len(self.all_spaces))
            print("self.empty_ratio: ", self.empty_ratio)
            agentWeight = random.gauss(self.weightDistribution["mean"], self.weightDistribution["sd"])  # give the agent a normally-distributed weight based on given mean and sd
            rational = True                 # TODO: CHANGE THIS TO BE BASED ON SOMETHING, NOT JUST TRUE ACROSS THE BOARD?
            stepTime = 1                    # TODO: CHANGE THIS TO BE BASED ON SOMETHING, NOT JUST 1 FOR EVERY AGENT?
            panicThreshold = 0.7            # TODO: CHANGE THIS TO BE BASED ON SOMETHING, NOT JUST 0.7 FOR EVERY AGENT?
            newAgent = Agent(agentWeight, rational, stepTime, panicThreshold) 
            self.agents.append(newAgent)

        print("agents: ", self.agents)

    def move_locations(self):
        total_distance = 0
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0
            
            for agent in self.old_agents: # each player moves one-by-one
                # TODO: PLAY A NORMAL-FORM GAME TO DETERMINE IF AGENT QUEUES/PUSHES, AND THUS IF PLAYER MOVES OR NOT, AND IF PLAYER FALLS OR NOT
                    # can use calculateCrowdDensity() to determine the crowd density around an agent
                    # then use agent.isRational(crowdDensity) to determine whether that agent is going to be rational or irrational
                continue

            if i%30==0:
                print('Iteration: %d , Number of changes: %d total distance: %d' %(n_changes, total_distance))
            
            if n_changes == 0:
                break

    def plot(self, title, file_name):
        # TODO: PLOT THE AGENTS ON THE GRAPH
        return

    def calculateCrowdDensity(self):
        # TODO: DETERMINE THE RATIO OF EMPTY SPACES TO OCCUPIED SPACES AROUND THE PLAYER
        # I'M THINKING THIS SHOULD BE FOR AT LEAST TWO RINGS AROUND THE PLAYER, IF NOT THREE
            # because just looking at the 9 squares immediately around a person doesn't seem like
            # enough to cause a person to panic
        return


def main():
    ##Starter Simulation
    weightDistribution = {"mean": 160, "sd": 20}  # not facts idk what weight distribution is
    stampede = Stampede(5, 5, 0.3, 200, weightDistribution)  # TODO: CHANGE THIS EVENTUALLY TO A BIGGER ARRAY :)
    stampede.populate()

    stampede.plot('Stampede Model: Initial State', 'stampede_initial.png')

    stampede.move_locations()

    stampede.plot('Stampede Model: Final State',
                     'stampede_final.png')


if __name__ == "__main__":
    main()