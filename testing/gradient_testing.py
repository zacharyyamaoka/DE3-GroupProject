import numpy as np
import unittest

import os
import sys
sys.path.append(os.path.join(os.getcwd(), "utils"))
sys.path.append(os.path.join(os.getcwd(), "solver"))


from Debugger import Debugger
from load_structure import *
from save_structure import *
from solver_util import *
from solver_func import *
# State vector
class TestMain(unittest.TestCase):

    def test_find_stability(self):
        K, L, X = loadFusionStructure("iso")
        # K, L, X = find_stability(K, L, X, Debugger, display_time=5)

    def test_converge_proper(self):
        debug = True
        K, L, X = loadFusionStructure("iso")
        step = 0.001
        print(K)
        self.assertEqual(np.sum(K-K.T),0)
        self.assertEqual(np.sum(L-L.T),0)
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
                # Debugger.draw_K_strut(K, L, X)
                Debugger.draw_C(D_i, K, L, X)
                Debugger.display(0.00001, 45, 20)

        if debug:
            Debugger.display(5, 45, 20)

        #export nodal positions to txt
        save_fusion360(X, K)



    def test_structure_loading(self):
        debug = False
        K, L, X = loadFusionStructure()
        n = K.shape[0]
        # print(K)
        # print(X)

        if debug:
            Debugger.clear()
            Debugger.draw_X(X)
            Debugger.draw_K_strut(K, L, X)
            Debugger.display(5, 45, 20)
        self.assertEqual(L.shape[0], n)
        self.assertEqual(X.shape[0], n)

    def test_X_to_D(self):
        nodes = 3
        X = np.zeros((nodes, 1, 3))
        X[0,0,0] = 1
        X[1,0,0] = 1
        X[2,0,0] = 3
        X[1,0,1] = 2
        D, cache1 = X_to_D(X)
        self.assertEqual(D[0,0],0)
        self.assertEqual(D[0,1],2)
        self.assertEqual(D[0,2],2)
        self.assertEqual(D[1,2],np.sqrt(2**2+2**2))

    def test_F(self):
       nodes = 2
       K = np.ones((nodes,nodes))
       X = np.zeros((nodes, 1, 3))
       L = np.zeros((nodes,nodes))
       X[0,0,0] = 0
       X[1,0,0] = 10
       D, cache1 = X_to_D(X)
       energy, cache = F(K,D,L)
       self.assertEqual(energy,50)

    def test_fusion_360(self):
        debug = False
        K, L, X = loadStructure()
        self.assertEqual(np.sum(K-K.T),0)

        iter = 2000
        for i in np.arange(iter):
            energy, cache = forward(K,X,L)
            D_3D, K_i, D_i, L_i = cache
            gradient, info = backprop(cache)
            X -= gradient * 0.01
            total_F, node_F = ForceInfo(K_i, D_i, L_i, D_3D)
            if (node_F < 1e-7).all():
                break
            if debug and i%100==0:
                Debugger.clear()
                Debugger.draw_X(X)
                Debugger.draw_C(D_i, K, L, X)
                Debugger.display(0.00001, 45, 20)
        if debug:
            Debugger.display(5, 45, 20)
    def test_force(self):
        debug = False
        nodes = 4

        K_s = 10 #careful with size of gradient
        L_s = 10.0

        L = np.array([[0, 0, L_s, 0],
                      [0, 0, 0, L_s],
                      [L_s, 0, 0, 0],
                      [0, L_s, 0, 0]])
        K = np.array([[0, 1, K_s, 1],
                    [1, 0, 1, K_s],
                    [K_s, 1, 0, 1],
                    [1, K_s, 1, 0]])

        X = np.random.normal(scale=3,size = (nodes, 1, 3))
        X[:,0,2] = 0 # set z value to zero


        iter = 1000
        for i in np.arange(iter):
            energy, cache = forward(K,X,L)
            D_3D, K_i, D_i, L_i = cache
            gradient, info = backprop(cache)
            X -= gradient * 0.01
            total_F, node_F = ForceInfo(K_i, D_i, L_i, D_3D)

            self.assertTrue(total_F < 1e-10)

            if debug:
                Debugger.clear()
                Debugger.draw_X(X)
                Debugger.draw_D(D_3D, X)
                # Debugger.draw_C(D_i, K, L, X)
                Debugger.display(0.0001)

        self.assertTrue((node_F < 1e-5).all())
    def test_tripod_formation(self): #not a real tensegrit structure, supports its self with its own struts
        debug = False
        nodes = 6

        K_s = 40 #careful with size of gradient
        L_s = 10.0

        K = np.array([[0, 1, 1, K_s, 1, 0],
                      [1, 0, 1, 0, K_s, 1],
                      [1, 1, 0, 1, 0, K_s],
                      [K_s, 0, 1, 0, 1, 1],
                      [1, K_s, 0, 1, 0, 1],
                      [0, 1, K_s, 1, 1, 0]])

        L = np.array([[0, 0, 0, L_s, 0, 0],
                      [0, 0, 0, 0, L_s, 0],
                      [0, 0, 0, 0, 0, L_s],
                      [L_s, 0, 0, 0, 0, 0],
                      [0, L_s, 0, 0, 0, 0],
                      [0, 0, L_s, 0, 0, 0]])

        X = np.random.normal(scale=3,size = (nodes, 1, 3))
        # X[:,0,2] = 0 # set z value to zero

        iter = 1000
        for i in np.arange(iter):
            energy, cache = forward(K,X,L)
            D_3D, K_i, D_i, L_i = cache
            gradient, info = backprop(cache)
            X -= gradient * 0.01
            total_F, node_F = ForceInfo(K_i, D_i, L_i, D_3D)
            if (node_F < 1e-4).all():
                self.assertTrue(True)
                break
            if debug:
                Debugger.clear()
                Debugger.draw_X(X)
                Debugger.draw_C(D_i, K, L, X)
                Debugger.display(0.00001, 45, 20)

        if i == iter-1:
            self.assertTrue(False)

    def test_X_formation(self):
        debug = False
        nodes = 4

        K_s = 10 #careful with size of gradient
        L_s = 10.0

        L = np.array([[0, 0, L_s, 0],
                      [0, 0, 0, L_s],
                      [L_s, 0, 0, 0],
                      [0, L_s, 0, 0]])
        K = np.array([[0, 1, K_s, 1],
                    [1, 0, 1, K_s],
                    [K_s, 1, 0, 1],
                    [1, K_s, 1, 0]])

        X = np.random.normal(scale=3,size = (nodes, 1, 3))
        X[:,0,2] = 0 # set z value to zero

        iter = 100
        for i in np.arange(iter):
            energy, cache = forward(K,X,L)
            D_3D, K_i, D_i, L_i = cache
            gradient, info = backprop(cache)
            grad_n = numerical_gradient(K, X, L, dx = 1e-6)
            for node in np.arange(nodes):
                for dim in np.arange(3):
                    error = rel_error(gradient[node,0,dim],grad_n[node,0,dim])
                    # check = error < 1e-7
                    check = error < 1e-5

                    if not check:
                        print(error)
                    self.assertTrue(check)
            X -= gradient * 0.01
            if debug:
                Debugger.clear()
                Debugger.draw_X(X)
                Debugger.draw_C(D_i, K, L, X)
                Debugger.display(0.0001)

    def test_gradient_descent(self):
        debug = False
        nodes = 10
        K = np.ones((nodes,nodes))
        L = np.zeros((nodes,nodes))
        X = np.zeros((nodes, 1, 3))
        X = np.random.normal(size = (nodes, 1, 3))
        iter = 100
        for i in np.arange(iter):
            energy, cache = forward(K,X,L)
            gradient, info = backprop(cache)
            grad_n = numerical_gradient(K, X, L, dx = 1e-4)
            for node in np.arange(nodes):
                for dim in np.arange(3):
                    error = rel_error(gradient[node,0,dim],grad_n[node,0,dim])
                    check = error < 1e-7
                    if not check:
                        print(error)
                    self.assertTrue(check)
            X -= gradient * 0.01
            if debug:
                Debugger.clear()
                Debugger.draw_X(X)
                Debugger.display(0.0001)

Debugger = Debugger()

if __name__ == '__main__':
    unittest.main()
