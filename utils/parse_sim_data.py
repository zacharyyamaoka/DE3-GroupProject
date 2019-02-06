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
cm_data_title = [col for col in data.columns if 'sense_bar' in col]
cm_data = data[cm_data_title].copy()
print(cm_data.head())

mixed_data = np.array(data)
pos = mixed_data[:,1:-1]
t = mixed_data[:,0]
dt = t[1] - t[0]
dt = 0.01
n = int(round(pos.shape[1]/7)) # x y z ax ay az m
full_data = dict()
scale = 10 #go from dm to m world
headers = list(data)
headers.pop(0)
for i in range(n):
    x = pos[:,i*7:((i+1)*7)-1]/scale

    pos_1 = i*7
    # print(headers[pos_1])
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
v4 = full_data['rod_4'][1][:,:3]
v4_norm = np.sqrt(np.sum(v4 * v4, axis = 1))
plt.figure(20)
plt.plot(t,v4_norm)

a4 = full_data['rod_4'][2][:,:3]
a4_norm = np.sqrt(np.sum(a4 * a4, axis = 1))
np.savetxt('./drop_data/a.txt', a4, fmt='%1.4f', delimiter=',')
plt.figure(2)
plt.plot(t,a4_norm)



# Collosion Info

max_a = np.max(a4_norm)
drop_height = 50/10 #100 dm
exp_t = np.sqrt(2*drop_height/9.81)
ax = plt.gca()
ax.set_xlim([exp_t-0.1,exp_t+0.1])
ax.text(0.9, 0.9, 'max: ' + str(round(max_a,3)) + " m/s^2", horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
if True:
    Viz.draw_Pos(full_data['rod_4'][0][:,:3])
    # Viz.draw_Pos(full_data['rod_1'][0][:,:3])
    # Viz.draw_Pos(full_data['rod_3'][0][:,:3])
    # Viz.draw_Pos(full_data['rod_2'][0][:,:3])
    # Viz.draw_Pos(full_data['rod_5'][0][:,:3])
    # Viz.draw_Pos(full_data['rod_4'][0][:,:3])
    Viz.display(time=1, azimuth=45, altitude=20, drop_port=True)

# plt.show()
plt.pause(100)
#a magnitude is a

# plt.plot(t,full_data['rod_1'][0][:,1])
# plt.show()
