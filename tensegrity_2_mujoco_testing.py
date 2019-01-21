import numpy as np
import unittest
from Debugger import Debugger
from load_structure import *
from save_structure import *
from solver_util import *
# could optimize to do half the computations but that is not where the greatest gain is
# Testing the 1 D Case
from mujoco_tensegrity import *


# State vector
class TestMain(unittest.TestCase):

    def test_2_mujoco(self):
        print(tensegrity_2_xml())

    def test_mujoco_tensegrity(self):
        run()

if __name__ == '__main__':
    unittest.main()
