import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

plt.ion()

# Code for doing a ruff order of magnitude estimation of inner spring constants, estimate ohw taht spring would behave



def estimate_spring_k(connection_points, e_k, max_f = 100):

    data = [[],[]]
    spring_k = 0

    #vectorize this
    cp = np.array(connection_points)
    n = cp.shape[0]
    cp_sum = np.sum(cp,axis=0)
    print(cp_sum.shape)
    #estimate position of payload for various additional forces
    for f in range(0,max_f):
        f_vec = np.array([0,-f,0])
        total = cp_sum - (f_vec/e_k)
        pos = total/n
        data[0].append(f)
        if f == 0: #eqn state:
            steady_state = pos
        data[1].append(abs(pos[1] - steady_state[1]))#net strain



    # Fit line

    #rise over run
    spring_k = data[0][n]/data[1][n]


    return data, spring_k #here data is a (nx2) array with (Force, delta_y) values, and K is the best fit line which describes the relation



connection_points = []
connection_points.append([1, 3, 0])
connection_points.append([-1, -3, 2])
connection_points.append([-2, -5, 2])


elastic_k = 2

data, spring_k = estimate_spring_k(connection_points, elastic_k)

fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111,projection='3d',proj_type = 'ortho')

for p in connection_points:
    ax1.scatter3D(p[0],p[1],p[2],'o')


fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)

ax2.plot(data[1],data[0])
ax2.set_title("Spring Constant: " + str(spring_k))
plt.show()
plt.pause(3)
