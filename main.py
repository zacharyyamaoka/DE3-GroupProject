from FormFinder import FormFinder
from Element import Element
from Structure import Structure
from Vizulization import Vizulization
import matplotlib.pyplot as plt
import numpy as np
Solver = FormFinder()

strut = Element(0, 0, 0, 0, 0, 0, 2)

# print(strut.getFrame()[0].shape)
# print(strut.getFrame()[1].shape)
# print(strut.getNodePos ition(1))
# print(Finder.solve(1))

drone = Structure(10,2)

plt.ion()
debug = False
wait = 0.1
Viz = Vizulization()

error_esp = 0.1
max_iter = 10000

iter = 0
energy = []
force = []

D, F, E, F_total, E_total = Solver.evalute(drone)
drone.max_element = np.argmax(F_total)
drone.max_force = np.amax(F_total)
drone.E_total = E_total
print(drone.C)

drone.C = np.array([[0, 1, 0, 1],
[1, 0, 1, 0],
[0, 1, 0, 1],
[1, 0, 1, 0]])

max_force = drone.max_force
while (max_force > error_esp) and (iter < max_iter):
    print(iter)
    iter += 1
    energy.append(E_total)
    force.append(max_force)
    max_force, E_total = Solver.update(drone)
    print(max_force)
    if debug:
        Viz.show(drone)
        plt.show()
        plt.pause(wait)


# Viz.F(drone)
print(energy)
print(force)
# Viz.show(drone)
# Viz.createGrid()
# plt.show()
# plt.pause(wait)
plt.close()
