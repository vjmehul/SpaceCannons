from SpaceCannons import SpaceCannons
import random
import csv
import random

env = SpaceCannons()
obs = env.reset()


episodes = 1000
i = 1
scores = []
demo = True
while i <= episodes:
    # action = []
    i = random.randint(0,4)
    n = random.randint(0,4)
    action=([i,n,demo])
    # print(action)
    # env.render()
    obs, global_reward_1, done, info = env.step(action)


