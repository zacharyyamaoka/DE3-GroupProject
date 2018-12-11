import os.path
import numpy as np

def loadStructure(filename = 'drone'):
    K_s = 50
    K_e = 1

    L_s = 10
    L_e = 0
    with open(os.path.join('/Users/zachyamaoka/Documents/de3_group_project/user_structures',filename), "r") as file1:
        lines = file1.readlines()
        K_mixed = np.fromstring(lines[0], dtype=int, sep=',')

    n = K_mixed.shape[0]
    nodes = int(np.sqrt(n))
    K_mixed = K_mixed.reshape(nodes,nodes)
    K = reOrderK(K_mixed, K_e, K_s)

    X = np.random.normal(scale=3,size = (nodes, 1, 3))
    # X[:,0,2] = 0 # set z value to zero

    L = np.zeros((nodes,nodes))
    L[K==K_s] = L_s
    L[K==K_e] = L_e

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
