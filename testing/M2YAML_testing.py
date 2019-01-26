import numpy as np
import unittest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), "utils"))
sys.path.append(os.path.join(os.getcwd(), "solver"))

from Debugger import Debugger
from load_structure import *
from save_structure import *
from solver_util import *
from solver_func import *

# could optimize to do half the computations but that is not where the greatest gain is
# Testing the 1 D Case

"""
# TODO:

0. Set up scale and size to match actual drone
1. Get meaning full and realistic data output
2. Smooth out flow for testing.
3. Generate Data Sheet

"""

Debugger = Debugger()
# State vector
class TestMain(unittest.TestCase):

    def test_fusion_2_yaml(self):
        file = 'iso'
        #Load up structure
        K, L, X = loadFusionStructure("iso")

        #find stability
        K, L, X = find_stability(K, L, X, Debugger, display_time=2)

        #Save back to YAML + Fusion 360

        save_YAML(X,K,file)
        save_DROP_YAML(file)
        save_fusion360(X, K)

    def test_save_DROP_YAML(self):
        file = 'iso'
        self.assertTrue(save_DROP_YAML(file))

    def test_GetKConstants(self):
        K, L, X = loadFusionStructure("iso")
        k_s, k_e = GetKConstants(K)
        self.assertEqual(k_s, 100)
        self.assertEqual(k_e, 5)

    def test_tensegrit_2_yaml(self):
        file = 'iso'
        K, L, X = loadFusionStructure(file)
        self.assertTrue(save_YAML(X,K,file))

        # the_dump = dump(t_info)
        # print(the_dump)
if __name__ == '__main__':
    unittest.main()
