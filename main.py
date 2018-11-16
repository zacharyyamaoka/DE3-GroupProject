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
debug = True
showViz = True
wait = 0.001
iterfreq = 500
checkin= False
checkinfreq = 100
checkinwait = 4
show = 1
error_esp = 0.001
max_iter = 5000

#Viz Stuff
Viz = Vizulization(3,3)
energy = []
force = []
fit_history = []

# EnergyGraph = Viz.createGraph()
# Viz.labelGraph(EnergyGraph,"EnergyGraph")
# ForceGraph = Viz.createGraph()
# Viz.labelGraph(ForceGraph,"ForceGraph")
FitnessGraph = Viz.createGraph()
Viz.labelGraph(FitnessGraph,"FitnessGraph")

def Solve(drone, ind):
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
        # energy.append(E_total)
        # force.append(max_force)
        max_force, E_total, sample_E = Solver.update(drone)
        # print("Energy: ", E_total)
        # print("Max Force: ", max_force)

        # if debug and iter%show==0:
        #     if iter%iterfreq==0:
        #         print(iter)
            # if drone.mutated:
            #     Viz.show(drone, ind)
            #     plt.pause(wait)
            # # Viz.F(drone)
            # Viz.plotGraph(EnergyGraph,E_total,iter)
            # Viz.plotGraph(ForceGraph,max_force,iter)
            # plt.show()
            # plt.pause(wait)
            # if checkin and iter%checkinfreq==0:
            #     plt.pause(checkinwait)
    # drone.solved = True
    if (iter >= max_iter):
        print("Over Iteration")
    Solver.reset() #for next time



max_gen = 1000
GA = Evolution(max_gen)
GA.initPop(20)

plt.show()

while GA.alive():
    print("----------------------")
    print("Curr Gen: ", GA.current_gen)
    print("Pop Size", len(GA.pop))
    for i in np.arange(len(GA.pop)):
        drone_structure = GA.pop[i][2]
        print(drone_structure.uniqueId)
        Solve(drone_structure, i) # drones have already been solved so they go very fast
        fit = GA.fitness(drone_structure)
        drone_structure.fitness = fit
        GA.addToQueue(drone_structure, fit)
    # Add functions to save popultion
    # For debugging
    max_fitness = GA.getMaxFitness()
    # print(max_fitness)
    if debug:
        # fit_history.append(max_fitness)

        if GA.current_gen%50==0:
            Viz.plotGraph(FitnessGraph,max_fitness,GA.current_gen)
            plt.pause(wait)

    if showViz:
        if GA.current_gen%50==0:
            total_length = len(GA.eval_pop)
            lenth = 9
            for i in np.arange(lenth):
                Viz.show(GA.eval_pop[total_length-i-1][2],i)
            plt.pause(wait)

    GA.remove(0.5) # percent to remove from orginal population
    GA.crossOver(0.5)
    GA.mutate(0.5)
    GA.nextGen()


for i in np.arange(len(GA.pop)):
    Viz.show(GA.pop[i][2],i)
# Solve(drone)
plt.pause(20)

plt.close()
