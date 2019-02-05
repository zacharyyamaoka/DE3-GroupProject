
#Deap Tutorial

from deap import base, creator, tools
import numpy as np
import random


"""Creater is used to make custom classes"""

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
#Creator takes 2 inputs. first is the name of class, second is base class it inherits from.
# The rest are custom parameters.

creator.create("Individual", list, fitness=creator.FitnessMin) #Creating a new type individual
#that is inheriting from the type list.


x = creator.Individual([123,123])
print(x.fitness.valid)
# I will use built in list b/c seems to have better functionality with this library

""" Register takes at least two arguments. It maps a function to a alias (function name).
Any values after thoose two are passed as arguments into the listed function"""

def testfunc():
    return 0

POP_SIZE = 100
NUM_BARS = 6

toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("testfunc", testfunc)
toolbox.register("individual", tools.initRepeat, container=creator.Individual,
func=toolbox.attr_float, n=1)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
pop = toolbox.population(n=10)
print(len(pop))

def initPopulation(pop_size, indv, num_bars):

    pop = []
    for i in range(pop_size):
        gene = indv(n=num_bars)
        pop.append(gene)

    return pop

toolbox.register("population_seed", initPopulation, pop_size=POP_SIZE, indv=toolbox.individual, num_bars=NUM_BARS)

pop = toolbox.population_seed()
print(pop[0].fitness.valid)
print(pop[0].fitness)

i1 = pop[0]

def evaluate(individual):
    return (sum(individual),)

fitness_i1 = evaluate(i1)

i1.fitness.values = fitness_i1

i2, = tools.mutGaussian(i1, mu=0.0, sigma=0.2, indpb=0.2)



i3 = pop[3]
i4 = pop[4]
print(i3)
tools.cxBlend(i3, i4, 0.5)
print(i3)



#very light weight wrapper, that then deals with some of the messy computation for me and forces me to stage the computation correctly
