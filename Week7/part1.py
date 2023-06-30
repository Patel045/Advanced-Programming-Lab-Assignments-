import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def yfunc(x):
    return x**2 + np.sin(8*x)


def simulated_anealling(yfunc,start,temperature,decay_rate):
    # Set up some large value for the best cost found so far
    bestcost = 100000
    # Generate several values within a search 'space' and check whether the new value is better
    # than the best seen so far.
    bestx = start
    rangemin, rangemax = -2, 2 
    xbase=np.linspace(rangemin,rangemax,1000)
    ybase=yfunc(xbase)
    fig, ax = plt.subplots()
    ax.plot(xbase, ybase)
    xall, yall = [], []
    lnall,  = ax.plot([], [], 'ro')
    lngood, = ax.plot([], [], 'go', markersize=10)
    def onestep(frame):
        nonlocal bestcost, bestx, decay_rate, temperature
        # Generate a random value \in -2, +2
        dx = (np.random.random_sample() - 0.5) * temperature
        x = bestx + dx
        # print(f"Old x = {x}, delta = {dx}")
        y = yfunc(x)
        if y < bestcost:
            # print(f"Improved from {bestcost} at {bestx} to {y} at {x}")
            bestcost = y
            bestx = x
            lngood.set_data(x, y)
        else:
            toss = np.random.random_sample()
            if toss < np.exp(-(y-bestcost)/temperature):
                bestcost = y
                bestx = x
                lngood.set_data(x, y)
            # print(f"New cost {y} worse than best so far: {bestcost}")
            pass
        temperature = temperature * decay_rate
        xall.append(x)
        yall.append(y)
        lnall.set_data(xall, yall)
        # return lngood,
    ani= FuncAnimation(fig, onestep, frames=range(100), interval=100, repeat=False)
    plt.show()

simulated_anealling(yfunc,-2,3,0.95)
