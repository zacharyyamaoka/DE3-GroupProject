from FormFinder import FormFinder
from Element import Element
from Structure import Structure
from Vizulization import Vizulization
import matplotlib as plt
Finder = FormFinder()

strut = Element(0, 0, 0, 0, 0, 0, 2)

# print(strut.getFrame()[0].shape)
# print(strut.getFrame()[1].shape)
# print(strut.getNodePosition(1))
# print(Finder.solve(1))

drone = Structure(10,10)

Viz = Vizulization()


print(drone.elements)
print(drone.nodes)
print(drone.C)
Viz.show(drone)
