# Each Player has these characteristics:
# strength/weakness: int amount (determined by weight, take normal distribution of average weight of the population)
# rational/irrational: t/f
# optimism/pessimism: might be same as rational/irrational
# step time: how long it takes them to walk somewhere

# rationality is determined by crowd density p(o \leq p \leq 1), where p is the degree of panic. when p is higher than a certain value, people become irrational.

# People are either optimistic or pessimistic. If optimistic, then the amount of crowd-press needed to make them irrational is higher. If optimism 


class Player:
    def __init__(self, weight, rational, stepTime, panicThreshold):
        self.weight = weight                    # Int: player's weight, assigned based on normal distribution from real population
        self.rational = rational                # Boolean: True for rational, False for irrational
        self.stepTime = stepTime                # Int: how long it takes the player to move somewhere
        self.panicThreshold = panicThreshold    # Int: the degree of panic at which the Player will switch from rational to irrational
        self.fallen = False                     # all players begin standing up
        self.timesTrampled = 0                  # if the player gets trampled twice they die, according to the study
        self.alive = True                       # all players begin alive... of course


    # Function that uses crowd density to determine whether the person is rational or irrational
    # crowdDensity: a float (0 <= crowdDensity <= 1) that represents the ratio of empty spaces to full spaces around the Player
    # crowdDensity is what we are using to represent the Player's degree of panic
    def isRational(self, crowdDensity, panicThreshold):
        degreeOfPanic = 
        if crowdDensity > 
