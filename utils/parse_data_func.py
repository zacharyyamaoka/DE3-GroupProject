import pandas as pd
import os
import glob
import numpy as np

import matplotlib.pyplot as plt
from Debugger import *

# Todo 3D postion vizulization
# To parse specific model name, then change its tag in the YAML so I can pick it out afterwards....

def get_max_a(a):
    a_norm = np.sqrt(np.sum(a * a, axis = 1))
    return np.max(a_norm), a_norm

def parse_data():
    #return x, v, a of cm
    path = os.path.join(os.getcwd(), "ntrt_sim_data/*")

    list_of_files = glob.glob(path) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)

    data = pd.read_csv(latest_file)

    mixed_data = np.array(data)
    pos = mixed_data[:,1:-1]
    t = mixed_data[:,0]
    dt = t[1] - t[0]
    dt = 0.01
    n = int(round(pos.shape[1]/7)) # x y z ax ay az m

    full_data = dict()
    scale = 10 #go from dm to m world

    for i in range(n):
        x = pos[:,i*7:((i+1)*7)-1]/scale

        pos_1 = i*7
        #switch y and z
        x_xyz = np.copy(x)
        x_xyz[:,1] = x[:,2]
        x_xyz[:,2] = x[:,1]
        x = x_xyz
        v = np.zeros_like(x)
        v[1:,:] = np.diff(x, axis=0)
        v /= dt

        a = np.zeros_like(v) #make sure to take acceleration as the different of dx/dt
        a[1:,:] = np.diff(v, axis=0)
        a /= dt

        full_data['rod_'+str(i)] = np.array([x,v,a])


    #just xyz
    x = full_data['rod_4'][0][:,:3]
    v = full_data['rod_4'][1][:,:3]
    a = full_data['rod_4'][2][:,:3]

    return t, x, v, a
