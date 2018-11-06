from StructureStructs import *
from Viz import *
from Simulator import *
import heapq


def GetFitness(drone):
    solveForces(drone)
    fitness = (1/drone.net_force) + drone.total_force * 10
    return 1


drones = []
# Create 100 different drone configurations and display tharctan2arctan2em

num_population = 4
epochs = 10
percent_clear = 0.5 # how many to get rid of
percent_mutate = 0.1 # of how many you keep how many do you mutate
percent_breed = 0.2 # of how many you keep how many do you breed?
show_viz = True
# Initalize population
for i in np.arange(num_population):
    num_node = np.random.randint(0,10,1)[0] #pick a random number of num_sticks
    drones.append(PaperDrone3D(num_node))

Vizulizer = Viz(drones, 3, 3)
Vizulizer.updateDrones(drones);
Vizulizer.showDrones(2);
# # Run Evolution
# for i in np.arange(epochs):
#
#     if (show_viz):
#         Vizulizer.updateDrones(drones);
#         Vizulizer.showDrones(2);
#
#     scores = []
#     eval_pop = []
#     count = 0
#     # evaluate current drones
#     for drone in drones:
#         solveForces(drone)
#         fitness = GetFitness(drone)
#         print(fitness)
#         heapq.heappush(eval_pop, (fitness, count, drone))
#         count += 1
#
#     # Evolution
#
#     num_keep = int(round((1-percent_clear)*num_population))
#     new_pop = []
#     for pop in heapq.nlargest(num_keep,eval_pop):
#         new_pop.append(pop[2])
#
#     for i in np.arange(num_population-num_keep):
#
#         p1 = new_pop[np.random.randint(0,num_keep)]
#         p2 = new_pop[np.random.randint(0,num_keep)]
#         child = p1.combine(p2)
#
#         #mutate child
#         if np.random.rand(1)[0] < percent_mutate:
#             child.mutate()
#
#         new_pop.append(child)
#
#     drones = new_pop
#
# # Create Vizulzation Matrix
#
# print("Net Force: ", drones[0].net_force)
# print("Total Force: ", drones[0].total_force)
# print("Check Force: ", drones[0].check_force)

#check FORCE NOT zero that is sketchy
plt.pause(2)
plt.close()
#! CAREFUL TO AVOID DESIGNS THAT HAVE NO BANDS SO THE TOTAL FORCE IS LOW.....
