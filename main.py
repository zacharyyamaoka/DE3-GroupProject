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


# print(drone.elements)
# print(drone.nodes)
# print(drone.C)
drone.F, drone.D = Solver.evalute(drone)

# Viz.show(drone)
Viz.F(drone)
Viz.show(drone)
plt.show()
plt.close()
