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

    def test_tensegrit_2_yaml(self):
        from yaml import load, dump

        t_info = dict()
        t_info["nodes"] = dict()
        t_info["nodes"][1] = [2, 3, 4]
        t_info["nodes"][2] = [2, 3, 4]
        t_info["nodes"][3] = [2, 3, 4]
        t_info["nodes"][4] = [2, 3, 4]

        t_info["pair_groups"] = dict()
        t_info["pair_groups"]["rod"] = [[1,2],[3,2],[4,2]]
        t_info["pair_groups"]["strut"] = [[1,2],[3,2],[4,2]]

        t_info["builders"] = dict()
        t_info["builders"]["prism_rod"] = dict()
        t_info["builders"]["prism_rod"]["class"] = "tgRodInfo"
        t_info["builders"]["prism_rod"]["parameters"] = dict()
        t_info["builders"]["prism_rod"]["parameters"]["denseity"] = 0.635
        t_info["builders"]["prism_rod"]["parameters"]["radius"] = 0.635
        


        the_dump = dump(t_info)
        print(the_dump)
if __name__ == '__main__':
    unittest.main()
