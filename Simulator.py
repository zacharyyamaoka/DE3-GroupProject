import numpy as np



def solveForces(drone):

    connections =  drone.connections
    num_sticks = drone.num_sticks

    for i in np.arange(num_sticks):
        net_force = np.zeros((6,1))
        start_stick = drone.sticks[i]

        node1 = np.array([start_stick.nodes[0].x,start_stick.nodes[0].y,0])
        node2 = np.array([start_stick.nodes[1].x,start_stick.nodes[1].y,0])
        cm = (node1 + node2)/2

        for j in connections[i]:

                end_id = int(j[2])
                c1 = int(j[0]) - 1
                c2 = int(j[1]) - 1
                end_stick = drone.sticks[end_id]

                start = np.array([start_stick.nodes[c1].x,start_stick.nodes[c1].y,0])
                end = np.array([end_stick.nodes[c2].x,end_stick.nodes[c2].y,0])

                dist_vec = start - end
                dist = np.sqrt(dist_vec.dot(dist_vec))
                force_vec = dist_vec * drone.elastic_constant
                lever_vec = cm - start
                torque_vec = np.cross(force_vec,lever_vec)
                net_force[0:3,0] += force_vec
                net_force[3:6,0] += torque_vec

            # print(np.ones((3,3)) / (2*np.ones((3,3))))

        start_stick.velocity_vec = net_force / start_stick.mass
        print(start_stick.velocity_vec)
        #solve for rotation and transloation velcity 6x1 vector
        #loop through each stick

def updatePostion(drone):
    dt = 0.01
    num_sticks = drone.num_sticks
    for i in np.arange(num_sticks):
        stick.velocity_vec = stick.acceleration * dt
        stick.position = stick.velocity_vec * dt + 0.5 * stick.acceleration * dt**2
