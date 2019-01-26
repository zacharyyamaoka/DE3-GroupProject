import numpy as np
import unittest
from Debugger import Debugger
from load_structure import *
from save_structure import *
from solver_util import *
# could optimize to do half the computations but that is not where the greatest gain is
# Testing the 1 D Case

"""
# TODO:

0. Set up scale and size to match actual drone
1. Get meaning full and realistic data output
2. Smooth out flow for testing.
3. Generate Data Sheet

"""
# State vector
class TestMain(unittest.TestCase):

    def test_GetKConstants(self):
        K, L, X = loadFusionStructure("1")
        k_s, k_e = GetKConstants(K)
        self.assertEqual(k_s, 100)
        self.assertEqual(k_e, 5)

    def test_tensegrit_2_yaml(self):
        K, L, X = loadFusionStructure("1")
        save_YAML(X,K,"drone_test_1")

        # the_dump = dump(t_info)
        # print(the_dump)
if __name__ == '__main__':
    unittest.main()
