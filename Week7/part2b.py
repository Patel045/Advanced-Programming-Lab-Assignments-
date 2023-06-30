import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

#File Reading 
def read_file(filename):
    x_cities=[]
    y_cities=[]
    with open(filename, 'r') as f:
        data=f.readlines()
        total_cities=int(data[0])
        for i in range(1,len(data)):
            x,y=data[i].split()
            x_cities.append(float(x))
            y_cities.append(float(y))
    x_cities=np.array(x_cities)
    y_cities=np.array(y_cities)
    return x_cities,y_cities,total_cities

#Function to give distance between 2 points
def dist(x1,y1,x2,y2):
    return np.sqrt(np.square(x2-x1)+np.square(y2-y1))

#Function to calculate total distance traversed by the given path
def calculate_cost(x_cities,y_cities,total_cities,order):
    distance=0
    for i in range(total_cities-1):
        distance+=dist(x_cities[order[i]],y_cities[order[i]],x_cities[order[i+1]],y_cities[order[i+1]])
    distance+=dist(x_cities[order[total_cities-1]],y_cities[order[total_cities-1]],x_cities[order[0]],y_cities[order[0]])
    return distance

def travelling_salesman(filename):
    x_cities,y_cities,total_cities=read_file(filename)
    #labels to name all the points on the graph
    labels=['P'+str(i) for i in range(total_cities)]
    # Initial temperature and decay rate
    T = 100.0
    decayrate = 0.99
    # Set up some large value for the best cost found so far
    bestcost = 10000000
    #Number of iteraions
    epoches=10000 
    #<Initialization>
    order=[i for i in range(total_cities)]
    random.shuffle(order)
    for epoch in range(epoches):
        # to get new order
        num_1=random.randint(0,total_cities)
        num_2=random.randint(0,total_cities)
        while(num_1==num_2):
            num_1=random.randint(0,total_cities)
            num_2=random.randint(0,total_cities)
        num1,num2=min(num_1,num_2),max(num_1,num_2)
        #<Perturbation>
        order=order[:num1]+order[num1:num2][::-1]+order[num2:]
        #calculate cost from the calculated order
        cost=calculate_cost(x_cities,y_cities,total_cities,order)
        #<Evaluation>
        if cost < bestcost:
            #<Acceptance>
            bestcost = cost
            final_order = order
        else:
            toss = np.random.random_sample()
            if toss < np.exp(-(cost-bestcost)/T):
                bestcost = cost
                final_order = order
            else:
               # get the original order
               order=order[:num1]+order[num1:num2][::-1]+order[num2:] 
        #<Cooling>
        T = T * decayrate
    #<Termination> of annealing
    print("The minimum distance is ",bestcost)
    print("Order :",final_order)
    xplot = x_cities[final_order] 
    yplot = y_cities[final_order]
    xplot = np.append(xplot, xplot[0])
    yplot = np.append(yplot, yplot[0])
    plt.plot(xplot, yplot, 'o-')
    for point in range(total_cities):
        plt.annotate(labels[point],xy=(x_cities[point],y_cities[point]))
    plt.show()

travelling_salesman("tsp_100.txt")
