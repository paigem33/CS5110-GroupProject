
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
        print("Populate ",  self.width ,  self.height)
        self.all_houses = list(itertools.product(range(self.width), range(self.height)))
        print(self.all_houses)
        random.shuffle(self.all_houses)


        self.n_empty = int(self.empty_ratio * len(self.all_houses))
        self.empty_houses = self.all_houses[:self.n_empty]
        #print(self.empty_houses)

        self.remaining_houses = self.all_houses[self.n_empty:]
        houses_by_color = [self.remaining_houses[i::self.colors] for i in range(self.colors)]
        print("Houses by color ", houses_by_color[0])
        for i in range(self.colors):
            # create agents for each color
            dict2 = dict(zip(houses_by_color[i], [i + 1] * len(houses_by_color[i])))
            self.agents = {**self.agents, **dict2}
        print("dictionary",self.agents)

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
            return float(count_similar) / (count_similar + count_different) < self.similarity_threshold

    def move_locations(self):
        total_distance=0
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0
            for agent in self.old_agents:
                if self.is_unsatisfied(agent[0], agent[1]):
                    agent_color = self.agents[agent]
                    empty_house = random.choice(self.empty_houses)
                    self.agents[empty_house] = agent_color
                    del self.agents[agent]
                    self.empty_houses.remove(empty_house)
                    self.empty_houses.append(agent)
                    total_distance += abs(empty_house[0] - agent[0])+ abs(empty_house[1] - agent[1])
                    n_changes += 1
            if i%30==0:
                print('Iteration: %d , Similarity Ratio: %3.2f. Number of changes: %d total distance: %d' %(i+1,self.similarity_threshold,n_changes,total_distance))
            if n_changes == 0:
                break

    # def move_to_empty(self, x, y):
    #     color = self.agents[(x, y)]
    #     empty_house = random.choice(self.empty_houses)
    #     self.updated_agents[empty_house] = color
    #     del self.updated_agents[(x, y)]
    #     self.empty_houses.remove(empty_house)
    #     self.empty_houses.append((x, y))

    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        # If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly
        agent_colors = {1: 'b', 2: 'r', 3: 'g', 4: 'c', 5: 'm', 6: 'y', 7: 'k'}
        marker_size = 150/self.width  # no logic here, I just played around with it
        for agent in self.agents:
            ax.scatter(agent[0] + 0.5, agent[1] + 0.5,s=marker_size, color=agent_colors[self.agents[agent]])

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

    def calculate_similarity(self):
        similarity = []
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
        return sum(similarity) / len(similarity)


def main():
    ##Starter Simulation
    schelling_0 = Schelling(5, 5, 0.3, 0.3, 200, 2)
    schelling_0.populate()

    ##First Simulation
    schelling_1 = Schelling(50, 50, 0.3, 0.3, 200, 2)
    schelling_1.populate()

    schelling_2 = Schelling(50, 50, 0.3, 0.5, 200, 2)
    schelling_2.populate()

    schelling_3 = Schelling(50, 50, 0.3, 0.8, 200, 2)
    schelling_3.populate()

    schelling_1.plot('Schelling Model with 2 colors: Initial State', 'schelling_2_initial.png')

    schelling_0.move_locations()
    schelling_1.move_locations()
    schelling_2.move_locations()
    schelling_3.move_locations()
    schelling_0.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 30%',
                     'schelling_0_30_final.png')
    schelling_1.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 30%',
                     'schelling_30_final.png')
    schelling_2.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 50%',
                     'schelling_50_final.png')
    schelling_3.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 80%',
                     'schelling_80_final.png')

    # #Second Simulation Measuring Seggregation
    # similarity_threshold_ratio = {}
    # for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    #     schelling = Schelling(50, 50, 0.3, i, 500, 2)
    #     schelling.populate()
    #     schelling.update()
    #     similarity_threshold_ratio[i] = schelling.calculate_similarity()
    #
    # fig, ax = plt.subplots()
    # plt.plot(similarity_threshold_ratio.keys(), similarity_threshold_ratio.values(), 'ro')
    # ax.set_title('Similarity Threshold vs. Mean Similarity Ratio', fontsize=15, fontweight='bold')
    # ax.set_xlim([0, 1])
    # ax.set_ylim([0, 1.1])
    # ax.set_xlabel("Similarity Threshold")
    # ax.set_ylabel("Mean Similarity Ratio")
    # plt.savefig('schelling_segregation.png')


if __name__ == "__main__":
    main()