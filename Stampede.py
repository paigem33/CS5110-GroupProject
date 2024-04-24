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
from A_star import Cell, A_Star

class Stampede:
    def __init__(self, width, height, fullRatio, n_iterations, weightDistribution):
        # self.agents = []                              # array: holds all agents               # TODO: RIGHT NOW THIS IS AN ARRAY, USED TO BE STORED IN {}; DECIDE IF THIS IS A GOOD DECISION OR IF IT SHOULD BE {}
        self.width = width                              # int: width of the grid I think
        self.height = height                            # int: height of the grid I think
        self.totalCells = width * height
        self.fullRatio = fullRatio                      # float
        self.n_iterations = n_iterations                # int
        self.weightDistribution = weightDistribution    # dictionary: { "mean": int, "sd": int }
        # all agents just need to get to row 0

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

    def calculateCrowdDensity(self):
        # TODO: DETERMINE THE RATIO OF EMPTY SPACES TO OCCUPIED SPACES AROUND THE PLAYER
        # I'M THINKING THIS SHOULD BE FOR AT LEAST TWO RINGS AROUND THE PLAYER, IF NOT THREE
            # because just looking at the 9 squares immediately around a person doesn't seem like
            # enough to cause a person to panic
        return
    

    def print_a_star_copy(self):
        print("a star copy: ")
        for row in self.a_star_copy:
            print(row)
    
    # this function takes one agent as a parameter
    # if it can find the first step the player should take, it returns a tuple of indices for that first step 
    # (first step is the location that the agent wants to go to next)
    def get_first_step(self, agent):
        self.a_star_copy = copy.deepcopy(self.agents)
        for i in range(len(self.a_star_copy)):
            for j in range(len(self.a_star_copy[i])):
                if self.a_star_copy[i][j] == '':
                    self.a_star_copy[i][j] = 0
                else:
                    self.a_star_copy[i][j] = 1
                
        # calculate the shortest path from this
        A_star = A_Star(self.height, self.width)
        firstStep = A_star.a_star_search(self.a_star_copy, [agent.position['y'], agent.position['x']])
        return firstStep

    def move_locations(self):
        total_distance = 0
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0
            
            for row in self.old_agents: # each player moves one-by-one
                for agent in row:
                    if agent != '': # if that spot isn't empty
                        print("agent coords: ", agent.position)
                        firstStep = self.get_first_step(agent)

                        if firstStep == None: # if the agent can't find a path to where they want to go
                            # move forward, or if you can't, then vvv
                            # play a normal-form game with the person in front of them
                            continue
                        else:
                            print("agent's first step is: ", firstStep) # this is in row, col order, so it'll look backwards to us
                
                # have players use a* to get to destination. 
                # if a* has no way of getting to destination, then have players play normal-form game with person in front of them 
                    # to see whether they push the person in front of them or queue
                    # if they push the person in front of them and that person queues, and they're stronger than the person they pushed, 
                    # then the players switch spots (and the weaker person is marked as fallen?)

                # TODO: PLAY A NORMAL-FORM GAME TO DETERMINE IF AGENT QUEUES/PUSHES, AND THUS IF PLAYER MOVES OR NOT, AND IF PLAYER FALLS OR NOT
                    # can use calculateCrowdDensity() to determine the crowd density around an agent
                    # then use agent.isRational(crowdDensity) to determine whether that agent is going to be rational or irrational
                continue
            
            if n_changes == 0:
                break

    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        # agent_colors = {1: 'b', 2: 'r'}
        agentColor = 'r'
        marker_size = 150 / self.width # no logic here, I just played around with it
        for row in self.agents:
            for agent in row:
                if (agent != ''):
                    if agent.fallen:
                        agentColor = 'b'
                    if not agent.alive:
                        agentColor = 'g'
                    ax.scatter(agent.position['x'] + 0.5, agent.position['y'] + 0.5, s=marker_size, color=agentColor) # TODO: CHANGE THIS TO BE COLORED BASED ON AGENT, NOT JUST RED ACROSS THE BOARD

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

        return
    
    # takes in two agents as params, agent1 and agent2
    # returns the strategy for each in the same order they were passed in
    # for example, play_normal_form_game(agent1, agent2) would return agent1Strategy, agent2Strategy
    def play_normal_form_game(self, agent1, agent2):
        if agent1.isRational() and agent1.weight < agent2.weight and agent2.isRational() and agent2.weight > agent1.weight:
            # Outcome for you: rational, weak; he: rational, strong
            outcomes = {
                ('queue', 'queue'): (0.8, 0.8),
                ('queue', 'push'): (0.2, 0.3),
                ('push', 'queue'): (0.2, 0.7),
                ('push', 'push'): (0.1, 0.3)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2
        
        if agent1.isRational() and agent1.weight > agent2.weight and agent2.isRational() and agent2.weight < agent1.weight:
            # Outcome for you: rational, strong; he: rational, weak
            outcomes = {
                ('queue', 'queue'): (0.7, 0.8),
                ('queue', 'push'): (0.2, 0.3),
                ('push', 'queue'): (0.5, 0.6),
                ('push', 'push'): (0.4, 0.1)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1.isRational() and not agent2.isRational() and agent1.weight < agent2.weight:
            # Outcome for you: irrational, weak; he: irrational, strong
            outcomes = {
                ('queue', 'queue'): (0.4, 0.3),
                ('queue', 'push'): (0.1, 0.5),
                ('push', 'queue'): (0.5, 0.3),
                ('push', 'push'): (0.7, 0.5)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1.isRational() and not agent2.isRational() and agent1.weight > agent2.weight:
            # Outcome for you: irrational, strong; he: irrational, weak
            outcomes = {
                ('queue', 'queue'): (0.3, 0.4),
                ('queue', 'push'): (0.1, 0.5),
                ('push', 'queue'): (0.7, 0.3),
                ('push', 'push'): (0.7, 0.5)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1.isRational() and agent2.isRational() and agent2.weight > agent1.weight:
            # Outcome for you: irrational, weak; he: rational, strong
            outcomes = {
                ('queue', 'queue'): (0.4, 0.9),
                ('queue', 'push'): (0.1, 0.4),
                ('push', 'queue'): (0.5, 0.8),
                ('push', 'push'): (0.5, 0.4)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1.isRational() and agent2.isRational() and agent2.weight < agent1.weight:
            # Outcome for you: irrational, strong; he: rational, weak
            outcomes = {
                ('queue', 'queue'): (0.3, 0.8),
                ('queue', 'push'): (0.3, 0.4),
                ('push', 'queue'): (0.7, 0.5),
                ('push', 'push'): (0.6, 0.3)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if agent1.isRational() and not agent2.isRational() and agent1.weight > agent2.weight:
            # Outcome for you: rational, strong; he: irrational, weak
            outcomes = {
                ('queue', 'queue'): (0.7, 0.4),
                ('queue', 'push'): (0.3, 0.5),
                ('push', 'queue'): (0.5, 0.3),
                ('push', 'push'): (0.5, 0.4)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if agent1.isRational() and not agent2.isRational() and agent1.weight < agent2.weight:
            # Outcome for you: rational, weak; he: irrational, strong
            outcomes = {
                ('queue', 'queue'): (0.8, 0.3),
                ('queue', 'push'): (0.3, 0.7),
                ('push', 'queue'): (0.3, 0.4),
                ('push', 'push'): (0.1, 0.6)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if agent1.isRational() and agent2.isRational() and agent1.weight == agent2.weight:
            # Outcome for you: rational; he: rational; Strong or weak
            outcomes = {
                ('queue', 'queue'): (0.9, 0.9),
                ('queue', 'push'): (0.2, 0.3),
                ('push', 'queue'): (0.3, 0.7),
                ('push', 'push'): (0.1, 0.1)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if agent1.isRational() and not agent2.isRational() and agent1.weight == agent2.weight:
            # Outcome for you: rational; he: irrational; Strong or weak
            outcomes = {
                ('queue', 'queue'): (0.8, 0.4),
                ('queue', 'push'): (0.3, 0.6),
                ('push', 'queue'): (0.5, 0.3),
                ('push', 'push'): (0.2, 0.5)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1.isRational() and agent2.isRational() and agent1.weight == agent2.weight:
            # Outcome for you: irrational; he: rational; Strong or weak
            outcomes = {
                ('queue', 'queue'): (0.4, 0.8),
                ('queue', 'push'): (0.6, 0.3),
                ('push', 'queue'): (0.3, 0.5),
                ('push', 'push'): (0.5, 0.2)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1.isRational() and not agent2.isRational() and agent1.weight == agent2.weight:
            # Outcome for you: irrational; he: irrational; Strong or weak
            outcomes = {
                ('queue', 'queue'): (0.4, 0.4),
                ('queue', 'push'): (0.1, 0.5),
                ('push', 'queue'): (0.6, 0.4),
                ('push', 'push'): (0.6, 0.6)
            }
            if agent1.isRational():
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2.isRational():
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2


def main():
    ##Starter Simulation
    weightDistribution = {"mean": 160, "sd": 20}  # not facts idk what weight distribution is
    stampede = Stampede(5, 5, 0.2, 200, weightDistribution)  # TODO: CHANGE THIS EVENTUALLY TO A BIGGER ARRAY :)
    stampede.populate()

    stampede.plot('Stampede Model: Initial State', 'stampede_initial.png')

    stampede.move_locations()

    stampede.print_a_star_copy()

    # stampede.move_locations()

    # stampede.plot('Stampede Model: Final State',
    #                  'stampede_final.png')


if __name__ == "__main__":
    main()