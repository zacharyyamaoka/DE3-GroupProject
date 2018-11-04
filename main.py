from StructureStructs import *
from Viz import *
from Simulator import *

drones = []
# Create 100 different drone configurations and display them

for i in range(1):
    num_sticks = np.random.randint(2,10,1)[0] #pick a random number of num_sticks
    num_sticks = 2
    drones.append(PaperDrone2D(num_sticks))



print(np.round(1.1))
print(np.round(1.6))

# Create Vizulzation Matrix

print(solveForces(drones[0]))
Vizulizer = Viz(drones,4,4)
Vizulizer.showDrones();



#! CAREFUL TO AVOID DESIGNS THAT HAVE NO BANDS SO THE TOTAL FORCE IS LOW.....
