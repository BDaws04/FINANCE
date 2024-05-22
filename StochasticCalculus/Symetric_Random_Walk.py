import numpy as np
import matplotlib.pyplot as plt

M = 10 #number of simulation
t = 10 #time

random_walk = [-1, 1]

steps = np.random.choice(random_walk, size=(M,t)).T
origin = np.zeros((1, M))
rw_paths = np.concatenate([origin, steps]).cumsum(axis=0)

plt.plot(rw_paths)
plt.xlabel("Years (t)")
plt.ylabel("Move")
plt.show()