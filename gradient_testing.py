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
       K = np.ones((nodes,nodes))
       X = np.zeros((nodes, 1, 3))
       X[0,0,0] = 0
       X[1,0,0] = 10
       D, cache1 = X_to_D(X)
       energy, cache = F(K,D)
       self.assertEqual(energy,50)
    def test_gradient(self):
        nodes = 2
        K = np.ones((nodes,nodes))
        X = np.zeros((nodes, 1, 3))
        X[0,0,0] = 0
        X[1,0,0] = 10

        D, cache1 = X_to_D(X)
        energy, cache = F(K,D)
        D_3D = cache1

        gradient = d_F(K, D_3D) #analytical Gradient
        # numerical gradient

        #forward difference,-> centered difference.
        dx = 1e-5
        X_n_f = np.copy(X)
        X_n_b = np.copy(X)

        X_n_f[1,0,0] += dx #take the steps seperatly, that is what your seeing with your analystical gradient.
        X_n_b[1,0,0] -= dx #take the steps seperatly, that is what your seeing with your analystical gradient.

        # dX = X_n - X
        # print(dX)
        D_n_f, cache1_n_f = X_to_D(X_n_f)
        energy_n, cache_n_f = F(K,D_n_f)

        
        dF = energy_n - energy
        gradient_n = dF / dx
        rel_error = abs(gradient[1,0,0] - gradient_n)/ np.maximum(abs(gradient[1,0,0]),abs(gradient_n))
        print(rel_error)
        self.assertTrue(rel_error < 1e-7)

Debugger = Debugger()

def X_to_D(X):
    num_nodes, n, c = X.shape
    full_X = np.tile(X,(1,num_nodes,1))
    X_T = X.reshape(1,num_nodes,3)
    full_X_T = np.tile(X_T,(num_nodes,1,1))
    D_3D = full_X_T - full_X
    D_1D = np.sqrt(np.sum((D_3D*D_3D),axis=2))
    cache = (D_3D)
    return D_1D, cache

def F(K, D):
    node_energy = 0.5 * K * D**2
    total_energy = np.sum(node_energy)/2 # to avoid double counting
    cache = (K, D)
    return total_energy, cache

nodes = 2
K = np.ones((nodes,nodes))
X = np.zeros((nodes, 1, 3))
X[0,0,0] = 0
X[1,0,0] = 10

D, cache1 = X_to_D(X)
energy, cache = F(K,D)
D_3D = cache1
print("displcae")
print(D_3D.shape)
print(D_3D[0])

def d_F(K, D_3D):
    n = K.shape[0]
    K_3D = K.reshape(n,n,1)
    M = K_3D * D_3D
    d = np.zeros((n,1,3))
    # print(M.shape)
    for i in np.arange(n):
        s = np.sum(M[:,i,:],axis=0,keepdims=True) - np.sum(M[i,:,:],axis=0,keepdims=True)
        s /= 2 #avoid double counting
        print(np.sum(M[i,:,:],axis=0,keepdims=True).shape)
        d[i,0,:] = s

    return d

print(energy)
gradient = d_F(K, D_3D)
print(gradient)
print(X)
X += gradient * 0.1 #we want to climb up the gradient.....
print(X)
# s = F(K,X)
Debugger.draw_X(X)
# Debugger.draw_D(s,X)

Debugger.display(0.1)

if __name__ == '__main__':
    unittest.main()
