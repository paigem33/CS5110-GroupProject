class Agent:
    def __init__(self, weight, rational, stepTime, panicThreshold):
        self.weight = weight                    # Int: agent's weight, assigned based on normal distribution from real population
        self.rational = rational                # Boolean: True for rational, False for irrational
        self.stepTime = stepTime                # Int: how long it takes the agent to move somewhere; eg. if agent has stepTime of 2 they can move UP TO 2 spaces during their turn and play AT MOST 2 normal form games?
        self.panicThreshold = panicThreshold    # Float: the ratio/degree of panic at which the Agent will switch from rational to irrational
        self.fallen = False                     # all agents begin standing up
        self.timesTrampled = 0                  # if the agent gets trampled twice they die, according to the study
        self.alive = True                       # all agents begin alive... of course

    # Function that uses crowd density to determine whether the person is rational or irrational
    # crowdDensity: a float (0 <= crowdDensity <= 1) that represents the ratio of empty spaces to full spaces around the Player
        # crowdDensity is what we are using to represent the Agent's degree of panic
    def isRational(self, crowdDensity):
        if crowdDensity > self.panicThreshold: 
            return False
        else:
            return True 

