from FormFinder import FormFinder
from Element import Element
from Structure import Structure
from Vizulization import Vizulization
from Evolution import Evolution

import matplotlib.pyplot as plt
import numpy as np

Solver = FormFinder()

plt.ion()

# Control Panel
debug = False
wait = 0.001

checkin= False
checkinfreq = 100
checkinwait = 4
show = 10
error_esp = 0.01
max_iter = 10000

#Viz Stuff
Viz = Vizulization(2,2)
energy = []
force = []
# EnergyGraph = Viz.createGraph()
# Viz.labelGraph(EnergyGraph,"EnergyGraph")
# ForceGraph = Viz.createGraph()
# Viz.labelGraph(ForceGraph,"ForceGraph")

def Solve(drone):
    # if (drone.solved):
    #     return

    iter = 0
    D, F, E, F_total, E_total = Solver.evalute(drone)

    drone.max_element = np.argmax(F_total)
    drone.max_force = np.amax(F_total)
    drone.E_total = E_total
    drone.F_total = F_total

    max_force = drone.max_force
    while (max_force > error_esp) and (iter < max_iter):
        iter += 1
        energy.append(E_total)
        force.append(max_force)
        max_force, E_total, sample_E = Solver.update(drone)
        print(iter)
        # print("Energy: ", E_total)
        # print("Max Force: ", max_force)

        if debug and iter%show==0:
            Viz.show(drone)
            # Viz.F(drone)
            Viz.plotGraph(EnergyGraph,E_total,iter)
            Viz.plotGraph(ForceGraph,max_force,iter)
            plt.show()
            plt.pause(wait)
            if checkin and iter%checkinfreq==0:
                plt.pause(checkinwait)
    # drone.solved = True
    Solver.reset() #for next time



max_gen = 10
GA = Evolution(max_gen)
GA.initPop(4)

while GA.alive():
    print("Curr Gen: ", GA.current_gen)

    for drone in GA.pop:
        drone_structure = drone[2]
        Solve(drone_structure) # drones have already been solved so they go very fast
        GA.addToQueue(drone_structure, GA.fitness(drone_structure))

    GA.remove(0.5) # percent to remove from orginal population
    GA.crossOver(0.5)
    GA.mutate(0.5)
    GA.nextGen()


for i in np.arange(len(GA.pop)):
    Viz.show(GA.pop[i][2],i)
print(len(GA.pop))
# Solve(drone)
# Viz.show(drone)
plt.pause(5)

plt.close()
