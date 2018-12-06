from FormFinder import FormFinder
from Element import Element
from Structure import Structure
from Vizulization import Vizulization
from Evolution import Evolution
from StructureFunction import *

import matplotlib.pyplot as plt
import numpy as np

A = Structure(10,3)
B = Structure(10,3)

Viz = Vizulization(1,2)

print(similar(A,B))
Viz.show(A, 1)
Viz.show(B, 0)

plt.show()
plt.close()
