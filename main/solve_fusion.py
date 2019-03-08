import numpy as np
import unittest

import os
import sys
sys.path.append(os.path.join(os.getcwd(), "utils"))
sys.path.append(os.path.join(os.getcwd(), "solver"))
sys.path.append('Users/zachyamaoka/Documents/de3_group_project/utils')

from Debugger import *
from load_structure import *
from save_structure import *
from solver_util import *
from solver_func import *
# State vector
Debugger = Debugger()
plt.ion()
K_s = 15000
K_e = 19*10
K, L, X = loadFusionStructure("drone_v4",strut_L = 0.44, strut_K=K_s, elastic_K=K_e, override_L=True)
K, L, X = find_stability(K, L, X, Debugger, display_time=0, step=0.00001, iter = 50000)
print("done")
save_fusion360(X, K)
overwrite_fusion360_file("drone_v4",X,K,L,K_s,K_e)
save_YAML(X,K,"drone_v22")
save_DROP_YAML("drone_v22",translation = [0, 50, 0]) # dm

# strut_K = 500, elastic_K = 50, strut_L = 0.3, elastic_L = 0
