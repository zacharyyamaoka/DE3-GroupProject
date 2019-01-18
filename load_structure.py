import os.path
import numpy as np


def load(filename, dtype):
    with open(os.path.join('/Users/zachyamaoka/Documents/de3_group_project/user_structures',filename), "r") as file1:
        lines = file1.readlines()
        info = np.fromstring(lines[0], dtype, sep=',')
    return info

def loadFusionStructure():
    K_s = -1
    K_e = 1

    L_s = 10
    L_e = 0

    K_mixed = load("droneK", int)
    L_mixed = load("droneL", float)
    X_mixed = load("droneX", float)
    n = K_mixed.shape[0] #see length of K matrix
    nodes = int(np.sqrt(n)) #there are n by n entries in K b/c its flat, #nodes is n
    K_mixed = K_mixed.reshape(nodes,nodes) #reshape into square matrix
    L_mixed = L_mixed.reshape(nodes,nodes) #reshape into square matrix
    X_mixed = X_mixed.reshape(nodes,3)

    K = K_mixed
    X = X_mixed
    L = L_mixed
    return K, L, X
loadFusionStructure()
def loadStructure(filename = 'droneK'):
    band_stiffness = 50
    strut_stiffness = 10
    K_s = -1
    K_e = 1

    L_s = 10
    L_e = 0
    with open(os.path.join('/Users/zachyamaoka/Documents/de3_group_project/user_structures',filename), "r") as file1:
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
