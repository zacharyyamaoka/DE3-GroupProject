import pandas as pd
import os
import glob
import numpy as np

import matplotlib.pyplot as plt
from Debugger import *

# Todo 3D postion vizulization
# To parse specific model name, then change its tag in the YAML so I can pick it out afterwards....


Viz = Debugger()
path = os.path.join(os.getcwd(), "ntrt_sim_data/*")

list_of_files = glob.glob(path) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

data = pd.read_csv(latest_file)
# print(data)

# print(data['0_rod(strut).X'])

mixed_data = np.array(data)
pos = mixed_data[:,1:-1]
t = mixed_data[:,0]
dt = t[1] - t[0]
n = int(pos.shape[1]/7) # x y z ax ay az m
print('timestamps: ', t.shape)
full_data = dict()
for i in range(n):
    x = pos[:,i*7:((i+1)*7)-1]

    #switch y and z
    x_xyz = np.copy(x)
    x_xyz[:,1] = x[:,2]
    x_xyz[:,2] = x[:,1]
    x = x_xyz
    print(x[1,:3])
    print(i*7,((i+1)*7)-1)
    v = np.zeros_like(x)
    v[1:,:] = np.diff(x, axis=0)
    a = np.zeros_like(v)

    a[1:,:] = np.diff(v, axis=0)

    v /= dt
    a /= dt

    full_data['rod_'+str(i)] = np.array([x,v,a])


#just xyz
a3 = full_data['rod_0'][2][:,:3]
a3_norm = np.sum(a3 * a3, axis = 1)

print(a3_norm.shape)
print(t.shape)

plt.figure(2)
plt.plot(t,a3_norm)
# plt.ylim((0,40))
plt.show()

if True:
    Viz.draw_Pos(full_data['rod_0'][0][:,:3])
    # Viz.draw_Pos(full_data['rod_1'][0][:,:3])
    # Viz.draw_Pos(full_data['rod_3'][0][:,:3])
    # Viz.draw_Pos(full_data['rod_2'][0][:,:3])
    # Viz.draw_Pos(full_data['rod_5'][0][:,:3])
    # Viz.draw_Pos(full_data['rod_4'][0][:,:3])
    Viz.display(time=1, azimuth=45, altitude=20, drop_port=True)


print(full_data['rod_3'][2].shape)

plt.pause(100)
#a magnitude is a

# plt.plot(t,full_data['rod_1'][0][:,1])
# plt.show()
