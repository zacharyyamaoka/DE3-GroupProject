from Debugger import Debugger
from load_structure import *
from solver_util import *
from Autodesk import ProjectDreamCatcher
from DroneFactory import DroneFactory
from genotype import encode, decode
import numpy as np

#Control Panel
num_struts = 6

params = {"max_gen":1000}

Factory = DroneFactory(num_struts)
new_pop = Factory.order(10)
GA = ProjectDreamCatcher(new_pop, encode, decode, **params)

print(GA.max_gen)

while GA.alive():
    GA.run()

    GA.show('fitness')
    GA.show('population')

    if GA.end():
        GA.kill()
