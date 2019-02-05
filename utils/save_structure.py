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

def save_DROP_YAML(filename='drone', height = 0, rotation = 0, translation = [0, 100, 0]):
    info = dict()
    info["substructures"] = dict()
    info["substructures"][filename] = dict()
    info["substructures"][filename]["path"] = "./" + filename
    info["substructures"][filename]["translation"] = translation
    info["substructures"][filename]["rotation"] = dict()
    info["substructures"][filename]["rotation"]["axis"] = [1, 0, 0]
    info["substructures"][filename]["rotation"]["angle"] = 45
    info["substructures"][filename]["scale"] = 1

    with open(os.path.join('./YAML',filename + "_drop"), "w") as file1:
        dump(info, file1)    # Write a YAML representation of data to 'document.yaml'.
        return True

def save_YAML(X,K,filename="drone"):
    info = dict()

    scale = 10 #make sure to set gravity to 98.1dm/s
    X *= scale
    K *= scale

    w = 0.079
    h = 0.079
    l = 0.079

    w *= scale
    h *= scale
    l *= scale

    r = 0.02 * np.sqrt(scale)
    r = 0.02*scale
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

                pos_1 = np.array(info["nodes"][one])
                pos_2 = np.array(info["nodes"][two])
                length = pos_1 - pos_2
                print(np.linalg.norm(length))
            if K[i,j] == K_e:
                elastic.append([one,two])

    info["pair_groups"]["strut"]=strut
    info["pair_groups"]["elastic"]=elastic

    # Add code to connect with payload
    #add payload nodes starting from n

    pay_nodes, payload, payload_bars = getPayload(w,h,l)

    for i in range(len(pay_nodes)):
        q = i + 1
        ind = "p" + str(q)

        info["nodes"][ind] = pay_nodes[i]


    # payload_bars = []
    # payload = []
    payload_connect = [["p1","node0"],["p1","node1"]]

    info["pair_groups"]["payload_bars"]=payload_bars
    info["pair_groups"]["payload"]=payload
    info["pair_groups"]["payload_connect"]=payload_connect

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
    info["builders"]["strut"]["parameters"]["radius"] = r #10 cm

    #Pay load t_info
    info["builders"]["payload_bars"] = dict()
    info["builders"]["payload_bars"]["class"] = "tgRodInfo"
    info["builders"]["payload_bars"]["parameters"] = dict()
    info["builders"]["payload_bars"]["parameters"]["density"] = 0.1
    info["builders"]["payload_bars"]["parameters"]["radius"] = r #10 cm

    info["builders"]["payload_connect"] = dict()
    info["builders"]["payload_connect"]["class"] = "tgBasicActuatorInfo"
    info["builders"]["payload_connect"]["parameters"] = dict()
    info["builders"]["payload_connect"]["parameters"]["stiffness"] = K_s
    info["builders"]["payload_connect"]["parameters"]["damping"] = 10
    info["builders"]["payload_connect"]["parameters"]["pretension"] = 10

    info["builders"]["payload"] = dict()
    info["builders"]["payload"]["class"] = "tgBoxInfo"
    info["builders"]["payload"]["parameters"] = dict()
    info["builders"]["payload"]["parameters"]["density"] = 0.5
    info["builders"]["payload"]["parameters"]["width"] = w/2 #10 cm
    info["builders"]["payload"]["parameters"]["height"] = h/2 #10 cm

    with open(os.path.join('./YAML',filename), "w") as file1:
        dump(info, file1)    # Write a YAML representation of data to 'document.yaml'.
        return True

def getPayload(width, height, length):
    nodes = []
    x1 = [length/2, 0, 0]
    x2 = [-length/2, 0, 0]
    y1 = [0, width/2, 0]
    y2 = [0, -width/2, 0]
    z1 = [0, 0, height/2]
    z2 = [0, 0, -height/2]

    nodes.append(x1)
    nodes.append(x2)
    nodes.append(y1)
    nodes.append(y2)
    nodes.append(z1)
    nodes.append(z2)

    box = [['p1','p2']]
    support = [['p1','p2'],['p1','p3'],['p1','p4'],['p1','p5'],['p1','p6']]

    return nodes, box, support
    #return box with proper node onnections


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
    path = os.path.join(os.getcwd(), "user_structures")
    with open(os.path.join(path,filename), "w") as file1:
        file1.write(info)
        file1.close()
