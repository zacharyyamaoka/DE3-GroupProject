import os.path
import numpy as np


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
