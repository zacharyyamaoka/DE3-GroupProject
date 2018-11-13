from FormFinder import FormFinder
from Element import Element
from Structure import Structure
from Vizulization import Vizulization
import matplotlib.pyplot as plt
Solver = FormFinder()

strut = Element(0, 0, 0, 0, 0, 0, 2)

# print(strut.getFrame()[0].shape)
# print(strut.getFrame()[1].shape)
# print(strut.getNodePos ition(1))
# print(Finder.solve(1))

drone = Structure(10,2)

Viz = Vizulization()

error_esp = 0.1
max_iter = 10
# print(drone.elements)
# print(drone.nodes)
# print(drone.C)
# iter = 0
# energy = []
# force = []
# Solver.solve(drone)

# while (max_force > error_esp) and (iter < max_iter):
Solver.solve(drone)
# drone.D, drone.F, E, F_total, E_total = Solver.evalute(drone)
# Viz.show(drone)
Viz.F(drone)
Viz.show(drone)
plt.show()
plt.close()
