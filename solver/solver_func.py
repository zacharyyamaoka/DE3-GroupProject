import numpy as np
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "utils"))

from Debugger import Debugger
from solver_util import *

def find_stability(K, L, X, Debugger=None, display_time=2):

        debug = False

        if Debugger:
            debug = True

        step = 0.001
        n = K.shape[0]
        iter = 3100
        for i in np.arange(iter):
            energy, cache = forward(K,X,L)
            D_3D, K_i, D_i, L_i = cache
            gradient, info = backprop(cache)
            X -= gradient * step
            total_F, node_F = ForceInfo(K_i, D_i, L_i, D_3D)
            if (abs(node_F) < 1e-12).all():
                break
            if iter % 1000 == 0 and iter != 0:
                step *= 0.1
            if debug and i%100==0:
                Debugger.clear()
                Debugger.draw_X(X)
                # Debugger.draw_payload(0.079, 0.079, 0.079) #potentially comment
                Debugger.draw_payload(0.50, 0.50, 0.50) #potentially comment
                # Debugger.draw_K_strut(K, L, X)
                Debugger.draw_C(D_i, K, L, X)
                Debugger.display(0.00001, 45, 20, )

        if debug:
            Debugger.display(display_time, 45, 20)
        return K, L, X
