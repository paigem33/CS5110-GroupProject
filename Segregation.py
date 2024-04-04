"""
Author : Adil Moujahid
Email : adil.mouja@gmail.com
Description: Simulations of Schelling's segregation model

You will need to set up pycharm to import matplotlib.
"""

import matplotlib.pyplot as plt
import itertools
import random
import copy


# I used Chat GPT to debug certain lines of code that I wrote.
class Schelling:
    def __init__(self, width, height, empty_ratio, similarity_threshold, n_iterations, colors=2):
        self.agents = None
        self.width = width
        self.height = height
        self.colors = colors
        self.empty_ratio = empty_ratio
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations

    def populate(self):
        self.empty_houses = []
        self.agents = {}
        print("Populate ", self.width, self.height)
        self.all_houses = list(itertools.product(range(self.width), range(self.height)))
        random.shuffle(self.all_houses)
        self.n_empty = int(self.empty_ratio * len(self.all_houses))
        self.empty_houses = self.all_houses[:self.n_empty]
        self.remaining_houses = self.all_houses[self.n_empty:]
        houses_by_color = [self.remaining_houses[i::self.colors] for i in range(self.colors)]
        for i in range(self.colors):
            # create agents for each color
            dict2 = dict(zip(houses_by_color[i], [i + 1] * len(houses_by_color[i])))
            self.agents = {**self.agents, **dict2}

    def is_unsatisfied(self, x, y):
        myColor = self.agents[(x, y)]
        count_similar = 0
        count_different = 0
        if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_houses:
            if self.agents[(x - 1, y - 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if y > 0 and (x, y - 1) not in self.empty_houses:
            if self.agents[(x, y - 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses:
            if self.agents[(x + 1, y - 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and (x - 1, y) not in self.empty_houses:
            if self.agents[(x - 1, y)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width - 1) and (x + 1, y) not in self.empty_houses:
            if self.agents[(x + 1, y)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height - 1) and (x - 1, y + 1) not in self.empty_houses:
            if self.agents[(x - 1, y + 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_houses:
            if self.agents[(x, y + 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_houses:
            if self.agents[(x + 1, y + 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1

        if (count_similar + count_different) == 0:
            return False
        else:

            return float(count_similar) / (count_similar + count_different) < self.similarity_threshold[myColor - 1]

    def close_empty_houses(self, x, y):
        emptyHouses = []
        if x > 0 and y > 0 and (x - 1, y - 1) in self.empty_houses:
            emptyHouses.append((x - 1, y - 1))
        if y > 0 and (x, y - 1) in self.empty_houses:
            emptyHouses.append((x, y - 1))
        if x < (self.width - 1) and y > 0 and (x + 1, y - 1) in self.empty_houses:
            emptyHouses.append((x + 1, y - 1))
        if x > 0 and (x - 1, y) in self.empty_houses:
            emptyHouses.append((x - 1, y))
        if x < (self.width - 1) and (x + 1, y) in self.empty_houses:
            emptyHouses.append((x + 1, y))
        if x > 0 and y < (self.height - 1) and (x - 1, y + 1) in self.empty_houses:
            emptyHouses.append((x - 1, y + 1))
        if x > 0 and y < (self.height - 1) and (x, y + 1) in self.empty_houses:
            emptyHouses.append((x, y + 1))
        if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) in self.empty_houses:
            emptyHouses.append((x + 1, y + 1))
        return emptyHouses

    def unsatisfied_neighbors(self, x, y):
        unsatisfiedNeighbors = []
        if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_houses and self.is_unsatisfied(x - 1, y - 1):
            unsatisfiedNeighbors.append((x - 1, y - 1))
        if y > 0 and (x, y - 1) not in self.empty_houses and self.is_unsatisfied(x, y - 1):
            unsatisfiedNeighbors.append((x, y - 1))
        if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses and self.is_unsatisfied(x + 1,
                                                                                                              y - 1):
            unsatisfiedNeighbors.append((x + 1, y - 1))
        if x > 0 and (x - 1, y) not in self.empty_houses and self.is_unsatisfied(x - 1, y):
            unsatisfiedNeighbors.append((x - 1, y))
        if x < (self.width - 1) and (x + 1, y) not in self.empty_houses and self.is_unsatisfied(x + 1, y):
            unsatisfiedNeighbors.append((x + 1, y))
        if x > 0 and y < (self.height - 1) and (x - 1, y + 1) not in self.empty_houses and self.is_unsatisfied(x - 1,
                                                                                                               y + 1):
            unsatisfiedNeighbors.append((x - 1, y + 1))
        if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_houses and self.is_unsatisfied(x, y + 1):
            unsatisfiedNeighbors.append((x, y + 1))
        if x < (self.width - 1) and y < (self.height - 1) and (
                x + 1, y + 1) not in self.empty_houses and self.is_unsatisfied(x + 1, y + 1):
            unsatisfiedNeighbors.append((x + 1, y + 1))
        return unsatisfiedNeighbors

    def move_locations(self):
        total_distance = 0
        agent_color = None
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0
            for agent in self.old_agents:
                agent_color = self.agents[agent]
                if self.is_unsatisfied(agent[0], agent[1]):
                    combined_lists = (self.close_empty_houses(agent[0], agent[1]) + self.unsatisfied_neighbors(agent[0],
                                                                                                               agent[
                                                                                                                   1]))
                    if len(combined_lists) == 0:
                        combined_lists = self.empty_houses
                    empty_house = random.choice(combined_lists)
                    if empty_house in self.empty_houses:
                        self.agents[empty_house] = agent_color
                        del self.agents[agent]
                        self.empty_houses.remove(empty_house)
                        self.empty_houses.append(agent)
                    else:
                        temp_agent = self.agents[agent]
                        self.agents[agent] = self.agents[empty_house]
                        self.agents[empty_house] = temp_agent
                    total_distance += abs(empty_house[0] - agent[0]) + abs(empty_house[1] - agent[1])
                    n_changes += 1
            if i % 30 == 0:
                if n_changes < i / 10:
                    print("Little change is being made so we're going to stop this. We had " + str(i) + " iterations.")
                    exit(-1)
                print('Iteration: %d , Similarity Ratio: %3.2f. Number of changes: %d total distance: %d' % (
                    i + 1, self.similarity_threshold[agent_color - 1], n_changes, total_distance))
            if n_changes == 0:
                break

    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        # If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly
        agent_colors = {1: 'b', 2: 'r', 3: 'g', 4: 'c', 5: 'm', 6: 'y', 7: 'k'}
        marker_size = 150 / self.width  # no logic here, I just played around with it
        for agent in self.agents:
            ax.scatter(agent[0] + 0.5, agent[1] + 0.5, s=marker_size, color=agent_colors[self.agents[agent]])

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

    def calculate_similarity(self):
        similarity = []
        color = None
        for agent in self.agents:
            count_similar = 0
            count_different = 0
            x = agent[0]
            y = agent[1]
            color = self.agents[(x, y)]
            if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_houses:
                if self.agents[(x - 1, y - 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if y > 0 and (x, y - 1) not in self.empty_houses:
                if self.agents[(x, y - 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses:
                if self.agents[(x + 1, y - 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and (x - 1, y) not in self.empty_houses:
                if self.agents[(x - 1, y)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and (x + 1, y) not in self.empty_houses:
                if self.agents[(x + 1, y)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and y < (self.height - 1) and (x - 1, y + 1) not in self.empty_houses:
                if self.agents[(x - 1, y + 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_houses:
                if self.agents[(x, y + 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_houses:
                if self.agents[(x + 1, y + 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            try:
                similarity.append(float(count_similar) / (count_similar + count_different))
            except:
                similarity.append(1)
        overThreshold = 0
        for i in similarity:
            if i >= self.similarity_threshold[color - 1]:
                overThreshold += 1
        print("The percentage of satisfied agents is " + str(overThreshold / len(self.agents)*100) + "%\n")


def main():
    # Starter Simulation
    schelling_0 = Schelling(5, 5, 0.3, [.5, .5], 200, 2)
    schelling_0.populate()
    schelling_0.move_locations()
    schelling_0.calculate_similarity()
    schelling_0.plot('Schelling Model with 2 colors: Final State', 'schelling_0_30_final.png')

    # First Simulation
    schelling_1 = Schelling(50, 50, 0.3, [.3, .33], 200, 2)
    schelling_1.populate()
    schelling_1.plot('Schelling Model with 2 colors: Initial State', 'schelling_2_initial.png')
    schelling_1.move_locations()
    schelling_1.calculate_similarity()
    schelling_1.plot('Schelling Model with 2 colors: Final State',
                     'schelling_30_final.png')

    # schelling_2 = Schelling(50, 50, 0.3, [.3,.8], 200, 2)
    # schelling_2.populate()
    # schelling_2.move_locations()
    # schelling_2.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 50%',
    #                  'schelling_50_final.png')

    # schelling_3 = Schelling(50, 50, 0.3, [.1,.4], 200, 2) schelling_3.populate() schelling_3.move_locations()
    # schelling_3.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 80%',
    # 'schelling_80_final.png')


if __name__ == "__main__":
    main()
