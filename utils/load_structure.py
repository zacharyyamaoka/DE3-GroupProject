import os.path
import numpy as np


def load(filename, dtype):
    with open(os.path.join('./user_structures',filename), "r") as file1:
        lines = file1.readlines()
        info = np.fromstring(lines[0], dtype, sep=',')
    return info
def reOrderKLX(K, L, X, K_e, K_s):
    n = K.shape[0]
    new_K = np.zeros((n,n))

    ind2loc = dict()
    loc2ind = dict()
    #first pass
    open_rows = list(range(n))
    pointer_a = 0
    pointer_b = int(n/2)
    #The first row will be the first row, and its connection will be the n/2 row
    for i in range(n):
        for j in range(n):
            if K[i,j] == K_s: #strut connection
                if i in open_rows:
                    ind2loc[i] = pointer_a #maps node num in old mat to node num in new map for base node
                    ind2loc[j] = pointer_b #maps node num in old mat to node num in new map for connection node
                    loc2ind[pointer_a] = i #maps node num in new mat to node num in old map
                    loc2ind[pointer_b] = j

                    new_K[pointer_a,pointer_b] = K_s #fill in new K
                    new_K[pointer_b,pointer_a] = K_s
                    # Essential says, I have dealth with nodes i and j, if they come up agian skip them
                    open_rows.remove(i) #avoid overriding rows
                    open_rows.remove(j) #avoid revisting old nodes

                    pointer_b += 1 #increment node ids in new K
                    pointer_a += 1

    for i in range(n):
        for j in range(n):
            if K[i,j] == K_e:
                new_i = ind2loc[i]
                new_j = ind2loc[j]
                new_K[new_i,new_j] = K_e

    #Transform L
    new_L = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            new_i = ind2loc[i]
            new_j = ind2loc[j]
            new_L[new_i,new_j] = L[i,j]

    #Transform X
    new_X = np.zeros((n,1,3))
    for i in range(n):
        new_i = ind2loc[i]
        new_X[new_i,:,:] = X[i,:,:]

    # will be symeterical at the end

    # loop through and fill in the other connections
    return new_K, new_L, new_X

def loadFusionStructure(filename = "drone", strut_K = 100, elastic_K = 5, strut_D = 1, elastic_L = 0):
    K_s = -1
    K_e = 1

    L_s = 0.3 #careful here.....
    L_e = 0
    K_mixed = load(filename + "_K", int)
    L_mixed = load(filename + "_L", float)
    X_mixed = load(filename + "_X", float)
    n = K_mixed.shape[0] #see length of K matrix
    nodes = int(np.sqrt(n)) #there are n by n entries in K b/c its flat, #nodes is n
    K_mixed = K_mixed.reshape(nodes,nodes) #reshape into square matrix
    L_mixed = L_mixed.reshape(nodes,nodes) #reshape into square matrix
    X_mixed = X_mixed.reshape(nodes,1,3)
    K, L, X = reOrderKLX(K_mixed, L_mixed, X_mixed, K_e, K_s)

    elastic_mask = K==K_e
    strut_mask = K==K_s
    K[strut_mask] = strut_K
    K[elastic_mask] = elastic_K
    L[strut_mask] = L_s
    L[elastic_mask] = L_e
    return K, L, X

def loadStructure(filename = 'drone_K'):
    band_stiffness = 1
    strut_stiffness = band_stiffness*4
    K_s = -1
    K_e = 1

    L_s = 10
    L_e = 0

    path = os.path.join(os.getcwd(), "user_structures")
    with open(os.path.join(path,filename), "r") as file1:
        lines = file1.readlines()
        K_mixed = np.fromstring(lines[0], dtype=int, sep=',')
    n = K_mixed.shape[0] #see length of K matrix
    nodes = int(np.sqrt(n)) #there are n by n entries in K b/c its flat, #nodes is n
    K_mixed = K_mixed.reshape(nodes,nodes) #reshape into square matrix
    K = reOrderK(K_mixed, K_e, K_s) #puts nodes that are connected with strut into the num_bar + position, like in UKF

    X = np.random.normal(scale=3,size = (nodes, 1, 3))
    # X[:,0,2] = 0 # set z value to zero

    L = np.zeros((nodes,nodes))
    L[K==K_s] = L_s
    L[K==K_e] = L_e

    K[K==K_s] = strut_stiffness
    K[K==K_e] = band_stiffness

    return K, L, X


def reOrderK(K, K_e, K_s):
    n = K.shape[0]
    new_K = np.zeros((n,n))

    ind2loc = dict()
    loc2ind = dict()
    #first pass
    open_rows = list(range(n))
    pointer_a = 0
    pointer_b = int(n/2)
    #The first row will be the first row, and its connection will be the n/2 row
    for i in range(n):
        for j in range(n):
            if K[i,j] == K_s: #strut connection
                if i in open_rows:
                    ind2loc[i] = pointer_a
                    ind2loc[j] = pointer_b
                    loc2ind[pointer_a] = i
                    loc2ind[pointer_b] = j

                    new_K[pointer_a,pointer_b] = K_s
                    new_K[pointer_b,pointer_a] = K_s
                    open_rows.remove(i)
                    open_rows.remove(j)

                    pointer_b += 1
                    pointer_a += 1

    for i in range(n):
        for j in range(n):
            if K[i,j] == K_e:
                new_i = ind2loc[i]
                new_j = ind2loc[j]
                new_K[new_i,new_j] = K_e

    # will be symeterical at the end

    # loop through and fill in the other connections
    return new_K

# K, L, X = loadStructure()
