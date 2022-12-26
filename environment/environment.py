import random
import numpy as np

class Environment(object):

    def __init__(self, size, ini_pellet_count):
        self.size = size
        self.ini_pellet_count = ini_pellet_count
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]

    def initialize(self):        
        locations = list()
        for r in range(1,self.size-1):
            for c in range(1,self.size-1):
                locations.append((r, c))
        random.shuffle(locations)
        self.pacman = locations.pop()
        self.pellets = set()
        for _ in range(self.ini_pellet_count):
            self.pellets.add(locations.pop())
        self.new_ghost()
        self.next_reward = 0
        self.pelletsconsumed = 0
    
    def new_ghost(self):
        (r, c) = self.pacman
        locations = [(r, self.size-2), (self.size-2, c), (r, 1), (1,c)]
        choice = random.choice(range(len(locations)))
        while(locations[choice]==(r,c)):
            locations = [(r, self.size-2), (self.size-2, c), (r, 1), (1,c)]
            choice = random.choice(range(len(locations)))
        self.ghost = locations[choice]
        self.ghost_action = self.directions[random.choice([0,1,2,3])]
    
    def display(self):
        for r in range(self.size):
            for c in range(self.size):
                if (r,c) == self.ghost:
                    print ('G',end =" ")
                elif (r,c) == self.pacman:
                    print ('O',end =" ")
                elif (r,c) in self.pellets:
                    print ('.',end =" ")
                elif r == 0 or r == self.size-1:
                    print ('X',end =" ")
                elif c == 0 or c == self.size-1:
                    print ('X',end =" ")
                else:
                    print (' ',end =" ")
            print()
        print()
    
    def actions(self):
        if self.terminal():
            return None
        else:
            return self.directions

    def terminal(self):
        if self.next_reward == -100:
            return True
        elif len(self.pellets) == 0:
            self.pellets = set()
            locations = list()
            for r in range(1,self.size-1):
                for c in range(1,self.size-1):
                    locations.append((r, c))
            random.shuffle(locations)
            p=np.random.randint(low=1, high=np.sqrt(self.size)+1)
            for count in range(p):
                self.pellets.add(locations.pop())
            return False
        else:
            return False
    
    def reward(self):
        return self.next_reward
        
    def update(self, action):
        pacman = self.pacman
        ghost = self.ghost
        (r, c) = self.pacman
        (dr, dc) = action
        self.pacman = (r+dr, c+dc)
        (r, c) = self.ghost
        (dr, dc) = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        self.ghost = (r+dr, c+dc)        
        (r, c) = self.ghost
        if r == 0 or r == self.size-1:
            self.new_ghost()
        elif c == 0 or c == self.size-1:
            self.new_ghost()
        (r,c) = self.pacman
        (gr,gc) = self.ghost
        if self.pacman == self.ghost:
            self.next_reward = -100
        elif (pacman, ghost) == (self.ghost, self.pacman):
            self.next_reward = -100
        elif r == 0 or r == self.size-1:
            self.next_reward = -100
        elif c == 0 or c == self.size-1:
            self.next_reward = -100
        elif self.pacman in self.pellets:
            self.next_reward = 10
            self.pelletsconsumed=self.pelletsconsumed+1
            self.pellets.remove(self.pacman)
        else:
            self.next_reward = -1

    def state(self):
        s = dict()
        sorted(self.pellets, key=lambda x:(x[0],x[1]))
        walls=[]
        temp=[0,self.size-1]
        for i in temp:
            for j in range(self.size):
                if([i,j] not in walls):
                    walls.append([i,j])
                if([j,i] not in walls):
                    walls.append([j,i])
        s['pelletsleft'] = len(self.pellets) / float(self.ini_pellet_count)
        s['walls'] = walls
        s['pacman'] = self.pacman
        s['ghost'] = self.ghost
        s['pellets'] = self.pellets
        return s