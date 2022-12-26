import random

class Agent(object):
    def __init__(self):
        self.epsilon = 0.1
        self.gamma = 0.99
        self.alpha = 0.01
        self.q=dict()

    def choose(self, s, actions):
        p = random.random()
        if p < self.epsilon:
            return random.choice(actions)
        else:
            return self.policy(s, actions)

    def policy(self, s, actions):
        max_value = max([self.Q(s,a) for a in actions])
        max_actions = [a for a in actions if self.Q(s,a) == max_value]
        return random.choice(max_actions)

    def Q(self, s, a):
        actions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]
        if(str([s,a]) not in self.q):
            for ac in actions:
                self.q[str([s,ac])] = 0
                # print(str([s,ac]))
        return self.q[str([s,a])]
    
    def update_q(self, s, a, sp, r, actions):
        actions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]
        max_value = max([self.Q(sp,ac) for ac in actions])
        max_actions=[ac for ac in actions if self.Q(sp,ac) == max_value]
        ap=random.choice(max_actions)
        self.q[str([s,a])]=self.Q(s,a)+self.alpha*(r+self.gamma*self.q[str([sp,ap])]-self.Q(s,a))