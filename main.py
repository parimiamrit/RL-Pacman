import os
import time
from environment.environment import Environment
from agents.q_agent import Agent
import matplotlib.pyplot as plt
import numpy as np

if __name__=='__main__':
    environment = Environment(5,1)
    agent = Agent()
    p=[]
    iterations=20000
    for episode in range(iterations):
        environment.initialize()
        while not environment.terminal():
            s = environment.state()
            actions = environment.actions()
            a = agent.choose(s, actions)
            environment.update(a)
            
            sp = environment.state()
            r = environment.reward()
            actions = environment.actions()
            agent.update_q(s, a, sp, r, actions)
            # print(environment.terminal())
        # print(environment.pelletsconsumed)
        p.append(environment.pelletsconsumed)
        if(episode%1000==0 and episode!=0):
            print(episode, len(agent.q))
    x=np.linspace(0, iterations,iterations)
    plt.plot(x,p)
    plt.show()

    # Testing the agent
    count=0
    testiter=10
    p=0
    while(count<testiter):
        environment.initialize()
        s = environment.state()
        print(len(agent.q))
        environment.display()
        agent.epsilon=0
        while not environment.terminal():
            s = environment.state()
            actions = environment.actions()
            a = agent.policy(s, actions)
            
            environment.update(a)
            time.sleep(0.25)
            os.system('cls')
            environment.display()
            print(count, environment.pelletsconsumed)
        count=count+1
        p=p+environment.pelletsconsumed
    print(p/testiter)