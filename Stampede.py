import matplotlib.pyplot as plt
import itertools
import datetime
import random
import copy
from Agent import Agent
from A_star import Cell, A_Star


# we need to return the number of agents that fell and the number that died
# show an image every few steps

class Stampede:
    def __init__(self, width, height, fullRatio, n_iterations, weightDistribution):
        self.width = width  # int: width of the grid I think
        self.height = height  # int: height of the grid I think
        self.totalCells = width * height
        self.fullRatio = fullRatio  # float
        self.n_iterations = n_iterations  # int
        self.weightDistribution = weightDistribution  # dictionary: { "mean": int, "sd": int }
        self.allAgents = []
        # all agents just need to get to row 0

    def populate(self):
        # Calculate the number of cells to fill with Agents
        numPlayerCells = int(self.totalCells * self.fullRatio)

        # Create an empty 2D array
        self.agents = [[''] * self.width for _ in range(self.height)]

        # Fill the array with Agents
        for _ in range(numPlayerCells):
            while True:
                agentWeight = random.gauss(self.weightDistribution["mean"], self.weightDistribution[
                    "sd"])  # give the agent a normally-distributed weight based on given mean and sd
                rational = True
                stepTime = 1
                panicThreshold = 0.7

                newAgent = Agent(agentWeight, rational, stepTime, panicThreshold)

                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

                if self.agents[y][x] == '':
                    self.agents[y][x] = newAgent  # fill a random "empty" spot in the array with a new agent
                    self.allAgents.append(newAgent)  # keep track of total agents for stats reasons
                    newAgent.position['x'] = x
                    newAgent.position['y'] = y
                    break

    def nine_square_ring(self, x,y):
        full_spots = 0
        # Lower left square
        if x-1 >= 0 and y-1 >= 0:
            if not self.agents[x-1][y-1] == '':
                full_spots += 1
        # Lower Square
        if y-1 >= 0 and x >= 0:
            if not self.agents[x][y-1] == '':
                full_spots += 1
        # Lower right square
        if x+1 <= (self.height - 1) and y-1 >= 0:
            if not self.agents[x+1][y-1] == '':
                full_spots += 1
        # Left square
        if x-1 >= 0 and y >= 0:
            if not self.agents[x-1][y] == '':
                full_spots += 1
        # Right square
        if x+1 <= (self.height - 1) and y >= 0:
            if not self.agents[x+1][y] == '':
                full_spots += 1
        # Upper Left square
        if x-1 >= 0 and y+1 <= (self.width - 1):
            if not self.agents[x-1][y+1] == '':
                full_spots += 1
        # Upper square
        if x >= 0 and y+1 <= (self.width - 1):
            if not self.agents[x][y+1] == '':
                full_spots += 1
        # Upper right square
        if x+1 <= (self.height - 1) and y+1 <= (self.width - 1):
            if not self.agents[x+1][y+1] == '':
                full_spots += 1
        return full_spots

    def sixteen_square_ring(self, x, y):
        full_spots = 0
        # Lowest leftest
        if x - 2 >= 0 and y - 2 >= 0:
            if not self.agents[x - 2][y - 2] == '':
                full_spots += 1
        # Lowest left
        if x - 1 >= 0 and y - 2 >= 0:
            if not self.agents[x - 1][y - 2] == '':
                full_spots += 1
        # Lowest
        if x >= 0 and y - 2 >= 0:
            if not self.agents[x][y - 2] == '':
                full_spots += 1
        # Lowest right
        if x + 1 <= (self.height - 1) and y - 2 >= 0:
            if not self.agents[x + 1][y - 2] == '':
                full_spots += 1
        # Lowest rightest
        if x + 2 <= (self.height - 1) and y - 2 >= 0:
            if not self.agents[x + 2][y - 2] == '':
                full_spots += 1
        # Lower leftest
        if x - 2 >= 0 and y - 1 >= 0:
            if not self.agents[x - 2][y - 1] == '':
                full_spots += 1
        # Lower rightest
        if x + 2 <= (self.width - 1) and y - 1 >= 0:
            if not self.agents[x + 2][y - 1] == '':
                full_spots += 1
        # Leftest
        if x - 2 >= 0 and y >= 0:
            if not self.agents[x - 2][y] == '':
                full_spots += 1
        # Rightest
        if x + 2 <= (self.height - 1) and y >= 0:
            if not self.agents[x + 2][y] == '':
                full_spots += 1
        # Higher leftest
        if x - 2 >= 0 and y + 1 <= (self.width - 1):
            if not self.agents[x - 2][y + 1] == '':  # CHANGE
                full_spots += 1
        # Higher rightest
        if x + 2 <= (self.height - 1) and y + 1 <= (self.width - 1):
            if not self.agents[x + 2][y + 1] == '':
                full_spots += 1
        # Highest leftest
        if x - 2 >= 0 and y + 2 <= (self.width - 1):
            if not self.agents[x - 2][y + 2] == '':
                full_spots += 1
        # Highest left
        if x - 1 >= 0 and y + 2 <= (self.width - 1):
            if not self.agents[x - 1][y + 2] == '':
                full_spots += 1
        # Highest
        if x >= 0 and y + 2 <= (self.width - 1):
            if not self.agents[x][y + 2] == '':
                full_spots += 1
        # Highest right
        if x + 1 <= (self.height - 1) and y + 2 <= (self.width - 1):
            if not self.agents[x + 1][y + 2] == '':
                full_spots += 1
        # Highest rightest
        if x + 2 <= (self.height - 1) and y + 2 <= (self.width - 1):
            if not self.agents[x + 2][y + 2] == '':
                full_spots += 1
        return full_spots

    def calculateCrowdDensity(self, x, y):
        result = (self.nine_square_ring(x, y) + self.sixteen_square_ring(x, y)) / 24
        return result

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
        n_changes_counter = 0
        round_counter = 0
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0

            for row in self.agents:  # each player moves one-by-one
                for agent in row:
                    if agent != '' and agent.alive:  # if that spot isn't empty
                        # print("agent coords: ", agent.position)
                        firstStep = self.get_first_step(agent)

                        if firstStep == None:  # if the agent can't find a path to where they want to go
                            # swap x,y coords so that the following logic vvv works:
                            # tempX = agent.position['x']
                            # agent.position['x'] = agent.position['y']
                            # agent.position['y'] = tempX

                            # move forward, or if you can't, then vvv
                            # play a normal-form game with the person in front of them
                            if agent.position['y'] != 0:  # if agent is not at the bottom row
                                other_agent = self.agents[agent.position['y'] - 1][agent.position['x']]
                                if self.agents[agent.position['y'] - 1][agent.position['x']] == '':
                                    # Move the agent forward if space is empty
                                    self.agents[agent.position['y'] - 1][agent.position['x']] = agent
                                    self.agents[agent.position['y']][agent.position['x']] = ''

                                    # update the agent to know its new location
                                    agent.position['y'] -= 1
                                    n_changes += 1  # Increment the change counter

                                elif self.agents[agent.position['y'] - 1][
                                    agent.position['x']] != '' and other_agent.alive:
                                    # Play a normal-form game
                                    agent_strategy, other_agent_strategy = self.play_normal_form_game(agent,
                                                                                                      other_agent)
                                    # game results
                                    if agent_strategy == 'queue' and other_agent_strategy == 'push':
                                        # since other agent is in front of our agent and our agent is queueing, nothing happens
                                        # it wouldn't make sense for the other agent to want to move backwards
                                        # so basically in this case the current agent just stays in place
                                        continue
                                    elif agent_strategy == 'push' and other_agent_strategy == 'queue':
                                        # if the agent weighs more than the other agent, they will trade spaces and other agent falls
                                        if agent.weight > other_agent.weight:  # Check if the current agent weighs more
                                            target_y = other_agent.position['y']
                                            target_x = other_agent.position['x']
                                            agent_starting_y = agent.position['y']
                                            agent_starting_x = agent.position['x']
                                            self.agents[target_y][target_x] = agent
                                            agent.position['y'] = target_y
                                            agent.position['x'] = target_x
                                            other_agent.fallen = True
                                            other_agent.timesTrampled += 1
                                            # if other agent has fallen twice then they die and don't move on the map
                                            if other_agent.timesTrampled == 2:
                                                other_agent.alive = False
                                            self.agents[agent_starting_y][agent_starting_x] = other_agent
                                            other_agent.position['y'] = agent_starting_y
                                            other_agent.position['x'] = agent_starting_x
                                            n_changes += 1  # Increment the change counter
                                        continue
                                    elif agent_strategy == 'push' and other_agent_strategy == 'push':
                                        # the agent that weighs more will win
                                        # if agent wins, then they will trade spaces with the other agent and the other agent falls
                                        # if other agent wins, they stay in place
                                        if agent.weight > other_agent.weight:  # Check if the current agent weighs more
                                            # If the current agent weighs more, trade places with the other agent
                                            target_y = other_agent.position['y']
                                            target_x = other_agent.position['x']
                                            agent_starting_y = agent.position['y']
                                            agent_starting_x = agent.position['x']
                                            self.agents[target_y][target_x] = agent
                                            agent.position['y'] = target_y
                                            agent.position['x'] = target_x
                                            other_agent.fallen = True
                                            other_agent.timesTrampled += 1
                                            # if other agent has fallen twice then they die and don't move on the map
                                            if other_agent.timesTrampled == 2:
                                                other_agent.alive = False
                                            self.agents[agent_starting_y][agent_starting_x] = other_agent
                                            other_agent.position['y'] = agent_starting_y
                                            other_agent.position['x'] = agent_starting_x

                                            n_changes += 1  # Increment the change counter
                                        elif agent.weight < other_agent.weight:  # Check if the other agent weighs more
                                            # If the other agent weighs more, no action needed, continue to the next agent
                                            continue
                                        continue
                                    elif agent_strategy == 'queue' and other_agent_strategy == 'queue':
                                        # if they both queue, nothing happens
                                        continue
                                else:
                                    target_y = other_agent.position['y']
                                    target_x = other_agent.position['x']
                                    agent_starting_y = agent.position['y']
                                    agent_starting_x = agent.position['x']
                                    other_agent.position['y'] = agent_starting_y
                                    other_agent.position['x'] = agent_starting_x
                                    self.agents[target_y][target_x] = agent
                                    self.agents[agent_starting_y][agent_starting_x] = other_agent

                                    n_changes += 1  # Increment the change counter

                            elif self.agents[agent.position['y']][agent.position['x']] != '':
                                # remove from agent list
                                self.agents[agent.position['y']][agent.position['x']] = ''
                                n_changes += 1  # Increment the change counter
                            else:
                                # has already been removed, do nothing
                                continue

                        else:
                            self.agents[agent.position['y']][agent.position['x']] = ''
                            self.agents[firstStep[0]][firstStep[1]] = agent
                            agent.position['y'] = firstStep[0]
                            agent.position['x'] = firstStep[1]
                            n_changes += 1  # Increment the change counter

            round_counter += 1

            if n_changes == 0:
                n_changes_counter += 1
            else:
                n_changes_counter = 0  # Reset the counter if changes were made

            # Check if no changes were made in consecutive iterations
            if n_changes_counter == 2:
                break

            if round_counter % 5 == 0:
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                self.plot('Stampede Model: move ' + str(timestamp), 'move_' + timestamp + '.png')

    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        marker_size = 150 / self.width  # no logic here, I just played around with it
        for agent in self.allAgents:
            agentColor = 'r'
            if agent.fallen:
                agentColor = 'b'
            if not agent.alive:
                agentColor = 'g'
            ax.scatter(agent.position['x'] + 0.5, agent.position['y'] + 0.5, s=marker_size,
                        color=agentColor)  # TODO: CHANGE THIS TO BE COLORED BASED ON AGENT, NOT JUST RED ACROSS THE BOARD

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)
        plt.close()

        return

    # takes in two agents as params, agent1 and agent2
    # returns the strategy for each in the same order they were passed in
    # for example, play_normal_form_game(agent1, agent2) would return agent1Strategy, agent2Strategy
    def play_normal_form_game(self, agent1, agent2):
        agent1_rational = agent1.isRational(self.calculateCrowdDensity(agent1.position['y'], agent1.position['x']))
        agent2_rational = agent2.isRational(self.calculateCrowdDensity(agent2.position['y'], agent2.position['x']))

        if agent1_rational and agent1.weight < agent2.weight and agent2_rational and agent2.weight > agent1.weight:
            # Outcome for you: rational, weak; he: rational, strong
            outcomes = {
                ('queue', 'queue'): (0.8, 0.8),
                ('queue', 'push'): (0.2, 0.3),
                ('push', 'queue'): (0.2, 0.7),
                ('push', 'push'): (0.1, 0.3)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent1_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if agent1_rational and agent1.weight > agent2.weight and agent2_rational and agent2.weight < agent1.weight:
            # Outcome for you: rational, strong; he: rational, weak
            outcomes = {
                ('queue', 'queue'): (0.7, 0.8),
                ('queue', 'push'): (0.2, 0.3),
                ('push', 'queue'): (0.5, 0.6),
                ('push', 'push'): (0.4, 0.1)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1_rational and not agent2_rational and agent1.weight < agent2.weight:
            # Outcome for you: irrational, weak; he: irrational, strong
            outcomes = {
                ('queue', 'queue'): (0.4, 0.3),
                ('queue', 'push'): (0.1, 0.5),
                ('push', 'queue'): (0.5, 0.3),
                ('push', 'push'): (0.7, 0.5)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1_rational and not agent2_rational and agent1.weight > agent2.weight:
            # Outcome for you: irrational, strong; he: irrational, weak
            outcomes = {
                ('queue', 'queue'): (0.3, 0.4),
                ('queue', 'push'): (0.1, 0.5),
                ('push', 'queue'): (0.7, 0.3),
                ('push', 'push'): (0.7, 0.5)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1_rational and agent2_rational and agent2.weight > agent1.weight:
            # Outcome for you: irrational, weak; he: rational, strong
            outcomes = {
                ('queue', 'queue'): (0.4, 0.9),
                ('queue', 'push'): (0.1, 0.4),
                ('push', 'queue'): (0.5, 0.8),
                ('push', 'push'): (0.5, 0.4)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1_rational and agent2_rational and agent2.weight < agent1.weight:
            # Outcome for you: irrational, strong; he: rational, weak
            outcomes = {
                ('queue', 'queue'): (0.3, 0.8),
                ('queue', 'push'): (0.3, 0.4),
                ('push', 'queue'): (0.7, 0.5),
                ('push', 'push'): (0.6, 0.3)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if agent1_rational and not agent2_rational and agent1.weight > agent2.weight:
            # Outcome for you: rational, strong; he: irrational, weak
            outcomes = {
                ('queue', 'queue'): (0.7, 0.4),
                ('queue', 'push'): (0.3, 0.5),
                ('push', 'queue'): (0.5, 0.3),
                ('push', 'push'): (0.5, 0.4)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if agent1_rational and not agent2_rational and agent1.weight < agent2.weight:
            # Outcome for you: rational, weak; he: irrational, strong
            outcomes = {
                ('queue', 'queue'): (0.8, 0.3),
                ('queue', 'push'): (0.3, 0.7),
                ('push', 'queue'): (0.3, 0.4),
                ('push', 'push'): (0.1, 0.6)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if agent1_rational and agent2_rational and agent1.weight == agent2.weight:
            # Outcome for you: rational; he: rational; Strong or weak
            outcomes = {
                ('queue', 'queue'): (0.9, 0.9),
                ('queue', 'push'): (0.2, 0.3),
                ('push', 'queue'): (0.3, 0.7),
                ('push', 'push'): (0.1, 0.1)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if agent1_rational and not agent2_rational and agent1.weight == agent2.weight:
            # Outcome for you: rational; he: irrational; Strong or weak
            outcomes = {
                ('queue', 'queue'): (0.8, 0.4),
                ('queue', 'push'): (0.3, 0.6),
                ('push', 'queue'): (0.5, 0.3),
                ('push', 'push'): (0.2, 0.5)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1_rational and agent2_rational and agent1.weight == agent2.weight:
            # Outcome for you: irrational; he: rational; Strong or weak
            outcomes = {
                ('queue', 'queue'): (0.4, 0.8),
                ('queue', 'push'): (0.6, 0.3),
                ('push', 'queue'): (0.3, 0.5),
                ('push', 'push'): (0.5, 0.2)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

        if not agent1_rational and not agent2_rational and agent1.weight == agent2.weight:
            # Outcome for you: irrational; he: irrational; Strong or weak
            outcomes = {
                ('queue', 'queue'): (0.4, 0.4),
                ('queue', 'push'): (0.1, 0.5),
                ('push', 'queue'): (0.6, 0.4),
                ('push', 'push'): (0.6, 0.6)
            }
            if agent1_rational:
                strategy1 = 'queue' if outcomes[('queue', 'queue')][0] > outcomes[('push', 'queue')][0] else 'push'
            else:
                strategy1 = 'push'
            if agent2_rational:
                strategy2 = 'queue' if outcomes[('queue', 'queue')][1] > outcomes[('queue', 'push')][1] else 'push'
            else:
                strategy2 = 'push'
            return strategy1, strategy2

    def results(self, agent_list):
        isDead = 0
        didFall = 0
        counter = 0
        for agent in agent_list:
            if (agent != ''):
                print("-----Agent " + str(counter) + "-----")
                print("Weight: " + str(agent.weight))
                print("Panic Threshold: " + str(agent.panicThreshold))
                print("Times Trampled: " + str(agent.timesTrampled))
                if agent.fallen:
                    print("Fallen? Yes")
                else:
                    print("Fallen? No")
                if agent.alive:
                    print("Alive? Yes")
                else:
                    print("Alive? No")
                print()
                if not agent.alive:
                    isDead += 1
                if agent.fallen:
                    didFall += 1
            counter += 1
        print("-------Total Stats-------")
        print("Total Dead Agents: " + str(isDead))
        print("Total Fallen Agents: " + str(didFall))


def main():
    ##Starter Simulation
    weightDistribution = {"mean": 160, "sd": 20}
    stampede = Stampede(9, 10, 0.9, 200, weightDistribution)
    stampede.populate()

    stampede.plot('Stampede Model: Initial State', 'stampede_initial.png')

    stampede.move_locations()

    stampede.results(stampede.allAgents)

    stampede.plot('Stampede Model: Final State',
                  'stampede_final.png')


if __name__ == "__main__":
    main()