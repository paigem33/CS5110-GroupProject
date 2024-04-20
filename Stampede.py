
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
    def __init__(self, width, height, fullRatio, n_iterations, weightDistribution):
        # self.agents = []                              # array: holds all agents               # TODO: RIGHT NOW THIS IS AN ARRAY, USED TO BE STORED IN {}; DECIDE IF THIS IS A GOOD DECISION OR IF IT SHOULD BE {}
        self.width = width                              # int: width of the grid I think
        self.height = height                            # int: height of the grid I think
        self.totalCells = width * height
        self.fullRatio = fullRatio                      # float
        self.n_iterations = n_iterations                # int
        self.weightDistribution = weightDistribution    # dictionary: { "mean": , "sd":  }

    def populate(self):
        # Calculate the number of cells to fill with Agents
        numPlayerCells = int(self.totalCells * self.fullRatio)

        # Create an empty 2D array
        self.agents = [[''] * self.width for _ in range(self.height)]

        # Fill the array with Agents
        for _ in range(numPlayerCells):
            while True:
                agentWeight = random.gauss(self.weightDistribution["mean"], self.weightDistribution["sd"])  # give the agent a normally-distributed weight based on given mean and sd
                rational = True                 # TODO: CHANGE THIS TO BE BASED ON SOMETHING, NOT JUST TRUE ACROSS THE BOARD?
                stepTime = 1                    # TODO: CHANGE THIS TO BE BASED ON SOMETHING, NOT JUST 1 FOR EVERY AGENT?
                panicThreshold = 0.7            # TODO: CHANGE THIS TO BE BASED ON SOMETHING, NOT JUST 0.7 FOR EVERY AGENT?
                
                newAgent = Agent(agentWeight, rational, stepTime, panicThreshold) 

                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

                if self.agents[y][x] == '':
                    self.agents[y][x] = newAgent  # fill a random "empty" spot in the array with a new agent
                    newAgent.position['x'] = x
                    newAgent.position['y'] = y
                    break

        # Print the array for funsies
        print("self.agents is: ", self.agents)

    def calculateCrowdDensity(self):
        # TODO: DETERMINE THE RATIO OF EMPTY SPACES TO OCCUPIED SPACES AROUND THE PLAYER
        # I'M THINKING THIS SHOULD BE FOR AT LEAST TWO RINGS AROUND THE PLAYER, IF NOT THREE
            # because just looking at the 9 squares immediately around a person doesn't seem like
            # enough to cause a person to panic
        return

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
            
            if n_changes == 0:
                break

    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        agent_colors = {1: 'b', 2: 'r'}
        marker_size = 150 / self.width # no logic here, I just played around with it
        for row in self.agents:
            for agent in row:
                if (agent != ''):
                    print("agent is: ", agent)
                    ax.scatter(agent.position['x'] + 0.5, agent.position['y'] + 0.5, s=marker_size, color='r') # TODO: CHANGE THIS TO BE COLORED BASED ON AGENT, NOT JUST RED ACROSS THE BOARD

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

        return


def main():
    ##Starter Simulation
    weightDistribution = {"mean": 160, "sd": 20}  # not facts idk what weight distribution is
    stampede = Stampede(5, 5, 0.3, 200, weightDistribution)  # TODO: CHANGE THIS EVENTUALLY TO A BIGGER ARRAY :)
    stampede.populate()

    stampede.plot('Stampede Model: Initial State', 'stampede_initial.png')

    # stampede.move_locations()

    # stampede.plot('Stampede Model: Final State',
    #                  'stampede_final.png')


if __name__ == "__main__":
    main()