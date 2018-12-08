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
showViz = True
updatefreq = 1

wait = 0.001
iterfreq = 25
checkin= False
checkinfreq = 100
checkinwait = 4
show = 1

# Solver Info
error_esp = 0.000001
max_iter = 2000
Solver = FormFinder(max_iter,error_esp)

#Viz Stuff
viz_row = 1
viz_col = 2
Viz = Vizulization(viz_row,viz_col)
energy = []
force = []
fit_history = []

if showViz:
    FitnessGraph = Viz.createGraph()
    Viz.labelGraph(FitnessGraph,"FitnessGraph")
    Viz.legendGraph(FitnessGraph,"Max Fitness",c="red")

population = 2
num_bars = 2
Viz.setStruts(num_bars)
#smaller stru  ts, less play but faster convergence.....
GA = Evolution(num_struts = num_bars, strut_length = 10, max_gen=1000,init_size =population, pop_size=population, mutation_rate=1, \
selection_rate = 0.1, selection_pressure = 1.85,elite_rate=0.2) #Essentailly just have an autmated hill climber rn, b/c mutation rate is so highself.
# GA.load()
GA.eps = 1
while GA.alive():
    print("----------------------")
    print("Curr Gen: ", GA.current_gen)
    print("Pop Size", len(GA.pop))

    for i in np.arange(len(GA.pop)):
        drone_structure = GA.pop[i][2] # loop through current population
        Solver.solve(drone_structure, i) # drones have already been solved so they go very fast
        fit = GA.fitness(drone_structure) # evaluate drone
        drone_structure.fitness = fit # update fitness
        GA.addToQueue(drone_structure, fit) # add drone the the queue
    # GA.niche()
    GA.rankQueue()

    if showViz:
        if GA.current_gen%updatefreq==0:
            Viz.plotGraph(FitnessGraph,GA.getMaxFitness(),GA.current_gen,c='red')
            Viz.plotGraph(FitnessGraph,GA.getAvgFitness(),GA.current_gen,c='black')
            plt.pause(wait)

        if GA.current_gen%updatefreq==0:
            total_length = len(GA.eval_pop)
            plots = min(total_length,viz_col*viz_row)
            for i in np.arange(plots):
                drone = GA.eval_pop[total_length-i-1][2]
                if drone.overIterated and i == 0:
                    print("GOING TO FALL!")
                Viz.show(drone,i) # show the top drones
            plt.pause(wait)
    if GA.current_gen % 250:
        GA.save()
    GA.elite() #p constant that first is selected.
    num_elite = len(GA.new_pop)
    GA.selection() #p constant that first is selected.
    num_selection = len(GA.new_pop) - num_elite
    GA.mutate(p_c = 0.1, p_reset = 0.1, p_mutateL = 0.1, step_c = 1, step_l = 0.1) #avoiding mutating the elites
    num_mutate = len(GA.new_pop) - num_elite - num_selection
    GA.crossOver()
    num_cross = len(GA.new_pop) - num_elite - num_selection - num_mutate
    GA.nextGen()
    print("Num elite: ", num_elite)
    print("Num Selection: ", num_selection)
    print("Num mutate: ", num_mutate)
    print("Num cross: ", num_cross)

total_length = len(GA.pop)
plots = min(total_length,viz_col*viz_row)
for i in np.arange(plots):
    Viz.show(GA.pop[i][2],i) # best are now at the front....

Viz.saveFigs()
plt.pause(5)
plt.close()
