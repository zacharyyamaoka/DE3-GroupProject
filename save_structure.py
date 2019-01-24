import os.path
import numpy as np
from yaml import *

def GetKConstants(K):

    list_full = K.flatten().tolist()
    list_unique = set(list_full)
    list_sorted = sorted(list_unique)
    k_e = list_sorted[1]
    k_s = list_sorted[2]
    return k_s,k_e

def save_YAML(X,K,filename="drone"):
    info = dict()

    scale = 10 #make sure to set gravity to 98.1dm/s

    X *= 10
    K *= 10

    n = X.shape[0]
    K_s, K_e = GetKConstants(K)
    #populate nodes
    info["nodes"] = dict()

    for i in range(n):
        ind = "node" + str(i)
        info["nodes"][ind] = X[i,0,:].tolist()

    info["pair_groups"] = dict()
    strut = []
    elastic = []
    for i in range(n):
        for j in range(i+1,n):
            one = "node" + str(i)
            two = "node" + str(j)
            if K[i,j] == K_s:
                strut.append([one,two])
            if K[i,j] == K_e:
                elastic.append([one,two])

    info["pair_groups"]["strut"]=strut
    info["pair_groups"]["elastic"]=elastic

    info["builders"] = dict()
    info["builders"]["elastic"] = dict()
    info["builders"]["elastic"]["class"] = "tgBasicActuatorInfo"
    info["builders"]["elastic"]["parameters"] = dict()
    info["builders"]["elastic"]["parameters"]["stiffness"] = K_s
    info["builders"]["elastic"]["parameters"]["damping"] = 10
    info["builders"]["elastic"]["parameters"]["pretension"] = 10

    info["builders"]["strut"] = dict()
    info["builders"]["strut"]["class"] = "tgRodInfo"
    info["builders"]["strut"]["parameters"] = dict()
    info["builders"]["strut"]["parameters"]["density"] = 0.635
    info["builders"]["strut"]["parameters"]["radius"] = 0.1

    with open(os.path.join('/Users/zachyamaoka/Documents/de3_group_project/YAML',filename), "w") as file1:
        dump(info, file1)    # Write a YAML representation of data to 'document.yaml'.

def save_fusion360(X, K):


    #center X
    n = X.shape[0]

    X_sum = np.sum(X, axis = (0, 1))
    X_avg = X_sum/n #middle point

    X = X - X_avg.reshape(1,1,3)
    X_sum = np.sum(X, axis = (0, 1))
    X_avg = X_sum/n

    X_info = ""
    K_info = ""

    last = n-1

    for i in range(n):
        row = X[i,0,:] * 100 #cm
        for j in range(3):
            X_info += str(row[j])
            if i != last:
                X_info += ","
            elif j != 2:
                X_info += ","
    for i in range(n):
        for j in range(n):

            K_info += str(k_Save_Val(K[i,j]))

            if i != last:
                K_info += ","
            elif j != last:
                K_info += ","


    save("fusion_drone_X", X_info)
    save("fusion_drone_K", K_info)

    return X_info

def k_Save_Val(val):
    # if int(val) == 10:
    #     val = 1
    # if int(val) == 50:
    #     val = -1
    return val

def save(filename, info):
    with open(os.path.join('/Users/zachyamaoka/Documents/de3_group_project/user_structures',filename), "w") as file1:
        file1.write(info)
        file1.close()
