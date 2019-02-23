import numpy as np

import matplotlib.pyplot as plt

# Code for doing a ruff order of magnitude estimation of inner spring constants, estimate ohw taht spring would behave



def estimate_spring_k(connection_points, elastic_k):

    data = [[0,1,2,3,4],[0,1,2,3,4]]
    spring_k = 0

    return data, spring_k #here data is a (nx2) array with (Force, delta_y) values, and K is the best fit line which describes the relation



connection_points = [1]
elastic_k = 1

data, spring_k = estimate_spring_k(connection_points, elastic_k)


plt.ion()
plt.plot(data[0],data[1])
plt.show()
plt.pause(1)
