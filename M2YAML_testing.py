import numpy as np
import unittest
from Debugger import Debugger
from load_structure import *
from save_structure import *
from solver_util import *
# could optimize to do half the computations but that is not where the greatest gain is
# Testing the 1 D Case
from mujoco_tensegrity import *
from yaml import *
from collections import OrderedDict
import os.path
"""
# TODO:

1. Tensegrity to YAML
2. YAML to simulator
3. Run Simulator

"""
# State vector
class TestMain(unittest.TestCase):

    def test_tensegrit_2_yaml(self):

        t_info = dict()
        t_info["nodes"] = dict()
        t_info["nodes"][1] = [2, 2, 4]
        t_info["nodes"][2] = [2, 10, 4]
        t_info["nodes"][3] = [2, 1, 4]
        t_info["nodes"][4] = [2, -5, 4]

        t_info["pair_groups"] = dict()
        t_info["pair_groups"]["rod"] = [[1,2],[3,2],[4,2]]
        t_info["pair_groups"]["strut"] = [[1,2],[3,2],[4,2]]

        t_info["builders"] = dict()
        t_info["builders"]["rod"] = dict()
        t_info["builders"]["rod"]["class"] = "tgRodInfo"
        t_info["builders"]["rod"]["parameters"] = dict()
        t_info["builders"]["rod"]["parameters"]["density"] = 0.635
        t_info["builders"]["rod"]["parameters"]["radius"] = 0.635

        t_info["builders"]["strut"] = dict()
        t_info["builders"]["strut"]["class"] = "tgRodInfo"
        t_info["builders"]["strut"]["parameters"] = dict()
        t_info["builders"]["strut"]["parameters"]["density"] = 0.635
        t_info["builders"]["strut"]["parameters"]["radius"] = 0.635
        # t_info = {"nodes":{1:[2]},"pair_groups":{},"builders":{}}

        with open(os.path.join('/Users/zachyamaoka/Documents/de3_group_project/YAML',"drone"), "w") as file1:
            # stream = file('document.yaml', 'w')
            dump(t_info, file1)    # Write a YAML representation of data to 'document.yaml'.
            print(dump(t_info))

        # the_dump = dump(t_info)
        # print(the_dump)
if __name__ == '__main__':
    unittest.main()
