import numpy as np
import unittest
from Debugger import Debugger
from load_structure import *
# could optimize to do half the computations but that is not where the greatest gain is
# Testing the 1 D Case

# State vector
class TestMain(unittest.TestCase):
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
        debug = True
        K, L, X = loadStructure()
        self.assertEqual(np.sum(K-K.T),0)

        iter = 1000
        for i in np.arange(iter):
            energy, cache = forward(K,X,L)
            D_3D, K_i, D_i, L_i = cache
            gradient, info = backprop(cache)
            X -= gradient * 0.01
            total_F, node_F = ForceInfo(K_i, D_i, L_i, D_3D)
            if (node_F < 1e-4).all():
                break
            if debug:
                Debugger.clear()
                Debugger.draw_X(X)
                Debugger.draw_C(D_i, K, L, X)
                Debugger.display(0.0001, 45, 20)

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

        K_s = 50 #careful with size of gradient
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
                Debugger.display(0.0001, 45, 20)

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

def ForceInfo(K, D, L, D_3D):
    n = K.shape[0]
    delta = D - L
    F = K * delta
    D = D.reshape(n,n,1)
    m = np.divide(D_3D, D, out=np.zeros_like(D_3D), where=D!=0)
    F_3D = m * F.reshape(n,n,1)
    F_nodes = np.sum(F_3D,axis=1)
    F_total = np.sum(F_nodes)

    return F_total, F_nodes

def forward(K,X,L):
    D, D_3D = X_to_D(X)
    energy_i, (K_i, D_i, L_i) = F(K,D,L)
    cache = (D_3D, K_i, D_i, L_i)

    return energy_i, cache

def backprop(cache):
    gradient = d_F(cache)
    info = (gradient)
    return gradient, info

Debugger = Debugger()

def rel_error(a, b):
    max = np.maximum(abs(a),abs(b))
    if max == 0:
        return 0
    return abs(a - b)/ max

def X_to_D(X):
    num_nodes, n, c = X.shape
    full_X = np.tile(X,(1,num_nodes,1))
    X_T = X.reshape(1,num_nodes,3)
    full_X_T = np.tile(X_T,(num_nodes,1,1))
    D_3D = full_X_T - full_X
    D_1D = np.sqrt(np.sum((D_3D*D_3D),axis=2))
    cache = (D_3D)
    return D_1D, cache

def F(K, D, L):
    delta = D - L
    node_energy = 0.5 * K * delta**2
    total_energy = np.sum(node_energy)/2 # to avoid double counting
    cache = (K, D, L)
    return total_energy, cache

def d_F(cache):
    D_3D, K, D, L = cache
    n = K.shape[0]
    m = np.divide(L, D, out=np.zeros_like(L), where=D!=0)
    c = (m) - 1 #accounts for inital length of bar
    c = c.reshape(n,n,1)
    K_3D = K.reshape(n,n,1)
    M = c * K_3D * D_3D
    d = np.zeros((n,1,3))
    for i in np.arange(n):
        s = np.sum(M[i,:,:],axis=0,keepdims=True) - np.sum(M[:,i,:],axis=0,keepdims=True)
        s /= 2 #avoid double counting
        d[i,0,:] = s

    return d

def numerical_gradient(K, X, L, dx = 1e-5):
    node, m, dim = X.shape
    gradient = np.zeros((node,m,dim))
    for i in np.arange(node):
        for j in np.arange(dim):
            X_n_f = np.copy(X)
            X_n_b = np.copy(X)

            X_n_f[i,0,j] += dx #take the steps seperatly, that is what your seeing with your analystical gradient.
            X_n_b[i,0,j] -= dx #take the steps seperatly, that is what your seeing with your analystical gradient.

            D_n_f, cache1_n_f = X_to_D(X_n_f)
            energy_n_f, cache_n_f = F(K,D_n_f,L)

            D_n_b, cache1_n_b = X_to_D(X_n_b)
            energy_n_b, cache_n_b = F(K,D_n_b,L)

            dF = energy_n_f - energy_n_b
            gradient_n = dF / (2*dx)
            gradient[i,0,j] = gradient_n

    return gradient

if __name__ == '__main__':
    unittest.main()
