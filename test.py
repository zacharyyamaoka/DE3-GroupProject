from FormFinder import FormFinder
from Element import Element
from Structure import Structure
from Vizulization import Vizulization
from Evolution import Evolution
from StructureFunction import *

import matplotlib.pyplot as plt
import numpy as np
K = np.array([[0,1,0,100,],[1,0,100,0,],[0,100,0,1,],[100,0,1,0,]])
print(K)
# A = Structure(10,3)
# B = Structure(10,3)
#
#
# GA = Evolution(num_struts = 2, strut_length = 10, max_gen=1000,init_size =10, pop_size=10, mutation_rate=0.1, \
# selection_rate = 0.5, selection_pressure = 1.8,elite_rate=0.1) #Essentailly just have an autmated hill climber rn, b/c mutation rate is so highself.
# GA.eps = 1
# GA.load(500)
# for i in np.arange(1000):
#     print(i)
#     print(GA.pop)
#     if i % 100 == 0:
#         GA.save(2)
#     GA.current_gen += 1
#
#
#
#
# Viz = Vizulization(1,2)
#
# print(similar(A,B))
# Viz.show(A, 1)
# Viz.show(B, 0)
