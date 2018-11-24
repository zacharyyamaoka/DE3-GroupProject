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
updatefreq = 1

wait = 0.001
iterfreq = 500
checkin= False
checkinfreq = 100
checkinwait = 4
show = 1
error_esp = 0.0001
max_iter = 5000

#Viz Stuff
viz_row = 4
viz_col = 4
Viz = Vizulization(viz_row,viz_col)
energy = []
force = []
fit_history = []

# EnergyGraph = Viz.createGraph()
# Viz.labelGraph(EnergyGraph,"EnergyGraph")
# ForceGraph = Viz.createGraph()
# Viz.labelGraph(ForceGraph,"ForceGraph")
FitnessGraph = Viz.createGraph()
Viz.labelGraph(FitnessGraph,"FitnessGraph")
Viz.legendGraph(FitnessGraph,"Max Fitness",c="red")
# Viz.legendGraph(FitnessGraph,"Avg Fitness",c="black")

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
        energy.append(E_total)
        force.append(max_force)
        max_force, E_total, sample_E = Solver.update(drone)
        # print("Energy: ", E_total)
        # print("Max Force: ", max_force)

        # if debug and iter%10==0:
        #     if iter%iterfreq==0:
        #         print(iter)
        #     # if drone.mutated:
        #     #     Viz.show(drone, ind)
        #     #     plt.pause(wait)
        #     # Viz.F(drone)
        #     Viz.show(drone, ind)
        #     Viz.plotGraph(Ene rgyGraph,E_total,iter)
        #     Viz.plotGraph(ForceGraph,max_force,iter)
        #     plt.show()
        #     plt.pause(0.01)
            # if checkin and iter%checkinfreq==0:
            #     plt.pause(checkinwait)
    # drone.solved = True
    if (iter >= max_iter):
        pass
        # print("Over Iteration")
    Solver.reset() #for next time

population = 20
GA = Evolution(max_gen=10, pop_size=population, mutation_rate=0.05, \
selection_rate = 0.4, selection_pressure = 1.8,elite_rate=0.1)
# GA.kill()

while GA.alive():
    print("----------------------")
    print("Curr Gen: ", GA.current_gen)
    print("Pop Size", len(GA.pop))

    for i in np.arange(len(GA.pop)):
        drone_structure = GA.pop[i][2] # loop through current population
        print(drone_structure.uniqueId)
        Solve(drone_structure, i) # drones have already been solved so they go very fast
        fit = GA.fitness(drone_structure) # evaluate drone
        drone_structure.fitness = fit # update fitness
        GA.addToQueue(drone_structure, fit) # add drone the the queue

    GA.rankQueue()

    if debug:
        # fit_history.append(max_fitness)

        if GA.current_gen%updatefreq==0:
            Viz.plotGraph(FitnessGraph,GA.getMaxFitness(),GA.current_gen,c='red')
            Viz.plotGraph(FitnessGraph,GA.getAvgFitness(),GA.current_gen,c='black')
            plt.pause(wait)

    if showViz:
        if GA.current_gen%updatefreq==0:
            total_length = len(GA.eval_pop)
            lenth = viz_row*viz_col
            for i in np.arange(lenth):
                Viz.show(GA.eval_pop[total_length-i-1][2],i) # show the top drones
            plt.pause(wait)

    print(GA.eval_pop)
    GA.selection() #p constant that first is selected.
    print(GA.new_pop)
    GA.mutate()
    GA.crossOver()
    print(GA.new_pop)
    GA.nextGen()



for i in np.arange(len(GA.pop)):
    Viz.show(GA.pop[i][2],i)
# Solve(drone)
plt.pause(5)
plt.close()
