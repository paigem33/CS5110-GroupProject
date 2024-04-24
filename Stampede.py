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
import heapq
from Agent import Agent


class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination


class Stampede:
    def __init__(self, width, height, fullRatio, n_iterations, weightDistribution):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination
        self.agents = []  # array: holds all agents               # TODO: RIGHT NOW THIS IS AN ARRAY, USED TO BE STORED IN {}; DECIDE IF THIS IS A GOOD DECISION OR IF IT SHOULD BE {}
        self.width = width  # int: width of the grid I think
        self.height = height  # int: height of the grid I think
        self.totalCells = width * height
        self.fullRatio = fullRatio  # float
        self.n_iterations = n_iterations  # int
        self.weightDistribution = weightDistribution  # dictionary: { "mean": , "sd":  }

    # Check if a cell is valid (aka within the grid)
    def is_valid(self, row, col):
        return 0 <= row < self.width and 0 <= col < self.height

    # Check if a cell is unblocked
    def is_unblocked(self, grid, row, col):
        return self.agents

    # Check if a cell is the destination
    def is_destination(self, row, col, dest):
        return row == dest[0] and col == dest[1]
    
    # Calculate the heuristic value of a cell (Euclidean distance to destination)
    def calculate_h_value(self, row, col, dest):
        return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

    # Implement the A* search algorithm
    def a_star_search(self, grid, src, dest):
        # Check if the source and destination are valid
        if not self.is_valid(src[0], src[1]) or not self.is_valid(dest[0], dest[1]):
            print("Source or destination is invalid")
            return

        # Check if the source and destination are unblocked
        if not self.is_unblocked(grid, src[0], src[1]) or not self.is_unblocked(grid, dest[0], dest[1]):
            print("Source or the destination is blocked")
            return

        # Check if we are already at the destination
        if self.is_destination(src[0], src[1], dest):
            print("We are already at the destination")
            return

        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(self.height)] for _ in range(self.width)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(self.height)] for _ in range(self.width)]

        # Initialize the start cell details
        i = src[0]
        j = src[1]
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Initialize the flag for whether destination is found
        found_dest = False

        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True

            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]

                # If the successor is valid, unblocked, and not visited
                if self.is_valid(new_i, new_j) and self.is_unblocked(grid, new_i, new_j) and not closed_list[new_i][
                    new_j]:
                    # If the successor is the destination
                    if self.is_destination(new_i, new_j, dest):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        print("The destination cell is found")
                        # Trace and print the path from source to destination
                        self.trace_path(cell_details, dest)
                        found_dest = True
                        return
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = self.calculate_h_value(new_i, new_j, dest)
                        f_new = g_new + h_new

                        # If the cell is not in the open list or the new f value is smaller
                        if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j

        # If the destination is not found after visiting all cells
        if not found_dest:
            print("Failed to find the destination cell")

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
                rational = True  # TODO: CHANGE THIS TO BE BASED ON SOMETHING, NOT JUST TRUE ACROSS THE BOARD?
                stepTime = 1  # TODO: CHANGE THIS TO BE BASED ON SOMETHING, NOT JUST 1 FOR EVERY AGENT?
                panicThreshold = 0.7  # TODO: CHANGE THIS TO BE BASED ON SOMETHING, NOT JUST 0.7 FOR EVERY AGENT?

                newAgent = Agent(agentWeight, rational, stepTime, panicThreshold)

                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

                if self.agents[y][x] == '':
                    self.agents[y][x] = newAgent  # fill a random "empty" spot in the array with a new agent
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

            for agent in self.old_agents:  # each player moves one-by-one
                # TODO: PLAY A NORMAL-FORM GAME TO DETERMINE IF AGENT QUEUES/PUSHES, AND THUS IF PLAYER MOVES OR NOT, AND IF PLAYER FALLS OR NOT
                # can use calculateCrowdDensity() to determine the crowd density around an agent
                # then use agent.isRational(crowdDensity) to determine whether that agent is going to be rational or irrational
                continue

            if n_changes == 0:
                break

    def plot(self, title, file_name):
        # TODO: PLOT THE AGENTS ON THE GRAPH
        return


def main():
    ##Starter Simulation
    weightDistribution = {"mean": 160, "sd": 20}  # not facts idk what weight distribution is
    stampede = Stampede(5, 5, 0.3, 200, weightDistribution)  # TODO: CHANGE THIS EVENTUALLY TO A BIGGER ARRAY :)
    stampede.populate()

    # stampede.plot('Stampede Model: Initial State', 'stampede_initial.png')

    # stampede.move_locations()

    # stampede.plot('Stampede Model: Final State',
    #                  'stampede_final.png')


if __name__ == "__main__":
    main()
