import unittest

from Debugger import Debugger
from load_structure import *
from solver_util import *
from Autodesk import ProjectDreamCatcher
from DroneFactory import DroneFactory
from genotype import encode, decode
import numpy as np

class TestProjectDreamCatcher(unittest.TestCase):

    def test_params(self):
        params = {"max_gen":1000}
        num_struts = 2
        Factory = DroneFactory(num_struts)
        new_pop = Factory.order(10)
        GA = ProjectDreamCatcher(new_pop, encode, decode, **params)
        self.assertEqual(GA.max_gen,1000)
        self.assertEqual(GA.encode(),0)
        self.assertEqual(GA.decode(),0)


    def test_decode(self):

if __name__ == '__main__':
    unittest.main()
