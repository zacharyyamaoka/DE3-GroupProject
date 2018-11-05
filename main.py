from StructureStructs import *
from Viz import *
from Simulator import *

drones = []
# Create 100 different drone configurations and display tharctan2arctan2em

for i in range(1):
    num_sticks = np.random.randint(2,10,1)[0] #pick a random number of num_sticks
    num_sticks = 2
    drones.append(PaperDrone2D(num_sticks))



print(np.round(1.1))
print(np.round(1.6))

# Create Vizulzation Matrix
Vizulizer = Viz(drones,1,1)

Vizulizer.showDrones();
print("looping")
solveForces(drones[0])
# print("outside:", drones[0].sticks[0].acceleration)
#
for i in range(1):
    solveForces(drones[0])
    updatePostion(drones[0])
    Vizulizer.showDrones();
    plt.pause(10)

#! CAREFUL TO AVOID DESIGNS THAT HAVE NO BANDS SO THE TOTAL FORCE IS LOW.....
