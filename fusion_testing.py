import numpy as np
import unittest
from Debugger import Debugger
from load_structure import *
from save_structure import *
from solver_util import *
# could optimize to do half the computations but that is not where the greatest gain is
# Testing the 1 D Case

# State vector
class TestMain(unittest.TestCase):
    def test_save_for_fusion(self):
        K, L, X = loadFusionStructure()
        save_fusion360(X, K)

Debugger = Debugger()


if __name__ == '__main__':
    unittest.main()
