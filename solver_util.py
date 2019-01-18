import numpy as np

# Forward functions
def forward(K,X,L):
    D, D_3D = X_to_D(X)
    energy_i, (K_i, D_i, L_i) = F(K,D,L)
    cache = (D_3D, K_i, D_i, L_i)

    return energy_i, cache

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

# Backward functions

def backprop(cache):
    gradient = d_F(cache)
    info = (gradient)
    return gradient, info

def rel_error(a, b):
    max = np.maximum(abs(a),abs(b))
    if max == 0:
        return 0
    return abs(a - b)/ max

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
