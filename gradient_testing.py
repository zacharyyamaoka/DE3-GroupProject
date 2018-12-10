import numpy as np
import unittest
from Debugger import Debugger
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

    def test_X_formationç(self):
        debug = True
        nodes = 4

        K_s = 100
        L_s = 10.0
        L = np.zeros((nodes,nodes))
        L = np.ones((nodes,nodes))*10

        L = np.array([[0, 0, L_s, 0],
                    [0, 0, 0, L_s],
                    [L_s, 0, 0, 0],
                    [0, L_s, 0, 0]])
        K = np.array([[0, 1, K_s, 1],
                    [1, 0, 1, K_s],
                    [K_s, 1, 0, 1],
                    [1, K_s, 1, 0]])
        K = np.ones((nodes,nodes))
        X = np.zeros((nodes, 1, 3))
        X = np.random.normal(scale=3,size = (nodes, 1, 3))
        X[:,0,2] = 0 # set z value to zero

        iter = 1000
        for i in np.arange(iter):
            energy, cache = forward(K,X,L)
            D_3D, K_i, D_i, L_i = cache
            gradient, info = backprop(cache)
            grad_n = numerical_gradient(K, X, L, dx = 1e-4)
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

    # def test_gradient_descent_2nodes(self):
    #     nodes = 2
    #     K = np.ones((nodes,nodes))
    #     L = np.zeros((nodes,nodes))
    #     Xs = []
    #     X = np.zeros((nodes, 1, 3))
    #     X[1,0,0] = 5
    #     X[1,0,1] = 5
    #     X[1,0,2] = -4
    #     Xs.append(X)
    #     X1 = np.copy(X)
    #     X1[0,0,0] = -1
    #     X1[0,0,1] = 2
    #     X1[0,0,2] = 3.4
    #     Xs.append(X1)
    #     X2 = np.random.normal(size = (nodes, 1, 3))
    #     Xs.append(X2)
    #
    #     for X in Xs:
    #         iter = 20
    #         for i in np.arange(iter):
    #             D, cache1 = X_to_D(X)
    #             energy, cache2 = F(K,D,L)
    #             K, D, L = cache2
    #             cache3 = (cache1, K, D, L)
    #             gradient = d_F(cache3)
    #             grad_n = numerical_gradient(K, X, L)
    #
    #             self.assertTrue(rel_error(gradient[0,0,0],grad_n[0,0,0]) < 1e-7)
    #             self.assertTrue(rel_error(gradient[0,0,1],grad_n[0,0,1]) < 1e-7)
    #             self.assertTrue(rel_error(gradient[0,0,2],grad_n[0,0,2]) < 1e-7)
    #             self.assertTrue(rel_error(gradient[1,0,0],grad_n[1,0,0]) < 1e-7)
    #             self.assertTrue(rel_error(gradient[1,0,1],grad_n[1,0,1]) < 1e-7)
    #             self.assertTrue(rel_error(gradient[1,0,2],grad_n[1,0,2]) < 1e-7)
    #             X += 0.01*gradient
    #             # Debugger.clear()
    #             # Debugger.draw_X(X)
    #             # Debugger.display(0.001)

    # def test_gradient(self):
    #     nodes = 2
    #     K = np.ones((nodes,nodes))
    #     X = np.zeros((nodes, 1, 3))
    #     L = np.zeros((nodes,nodes))
    #     X[0,0,0] = 0
    #     X[1,0,0] = 5
    #     energy, cache = forward(K,X,L)
    #     gradient, info = backprop(cache) # analttical gradient
    #     # numerical gradient
    #
    #     #forward difference,-> centered difference.
    #     dx = 0.0001
    #     X_n_f = np.copy(X)
    #     X_n_b = np.copy(X)
    #
    #     X_n_f[1,0,0] += dx #take the steps seperatly, that is what your seeing with your analystical gradient.
    #     X_n_b[1,0,0] -= dx #take the steps seperatly, that is what your seeing with your analystical gradient.
    #
    #     D_n_f, cache1_n_f = X_to_D(X_n_f)
    #     energy_n_f, cache_n_f = F(K,D_n_f)
    #     energy, cache = forward(K,X_n_f,L)
    #     gradient, info = backprop(cache)
    #
    #     D_n_b, cache1_n_b = X_to_D(X_n_b)
    #
    #     energy_n_b, cache_n_b = F(K,D_n_b)
    #     dF = energy_n_f - energy_n_b
    #     gradient_n = dF / (2*dx)
    #     rel_error = abs(gradient[1,0,0] - gradient_n)/ np.maximum(abs(gradient[1,0,0]),abs(gradient_n))
    #     self.assertTrue(rel_error < 1e-7)


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
