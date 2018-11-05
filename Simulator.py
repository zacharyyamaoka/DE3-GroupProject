import numpy as np
from StructureStructs import *



def solveForces(drone):

    connections =  drone.connections
    num_sticks = drone.num_sticks

    for i in np.arange(num_sticks):
        net_force = np.zeros((6,1))
        total_force = np.zeros((6,1))
        start_stick = drone.sticks[i]
        cm = start_stick.position[0:3,0]
        for j in connections[i]:

                end_id = int(j[2])
                c1 = int(j[0]) - 1
                c2 = int(j[1]) - 1
                end_stick = drone.sticks[end_id]
                #
                # if c1 = 0:
                #     start = node1[0:3,0]
                # else:
                #     start = node2[0:3,0]

                start = np.array([start_stick.nodes[c1].x,start_stick.nodes[c1].y,0])
                end = np.array([end_stick.nodes[c2].x,end_stick.nodes[c2].y,0])

                dist_vec = start - end
                dist = np.sqrt(dist_vec.dot(dist_vec))
                force_vec = dist_vec * drone.elastic_constant
                lever_vec = cm - start
                torque_vec = np.cross(force_vec,lever_vec)
                net_force[0:3,0] += force_vec
                net_force[3:6,0] += torque_vec
                total_force[0:3,0] += np.abs(force_vec)
                total_force[3:6,0] += np.abs(torque_vec)
            # print(np.ones((3,3)) / (2*np.ones((3,3))))

        drone.sticks[i].net_force = net_force
        drone.sticks[i].total_force = total_force
        drone.sticks[i].acceleration = net_force / start_stick.mass

        drone.net_force += np.sum(np.abs(net_force))
        drone.total_force += np.sum(total_force)
        drone.check_force += net_force
        # print("Accel: ", drone.sticks[i].acceleration)
        #solve for rotation and transloation velcity 6x1 vector
        #loop through each stick

def updatePostion(drone):
    dt = 0.001
    num_sticks = drone.num_sticks
    for i in np.arange(num_sticks):
        print(drone.sticks[i].position)

        drone.sticks[i].velocity += drone.sticks[i].acceleration * dt
        drone.sticks[i].position += drone.sticks[i].velocity * dt + 0.5 * drone.sticks[i].acceleration * dt**2

        # drone.sticks[i].node1 +=
        # print("z theta:", drone.sticks[i].position[5,0])
        print("position before")
        print(drone.sticks[i].position)
        offset = np.array([np.cos(drone.sticks[i].position[5,0]) * drone.sticks[i].length/2,
        np.sin(drone.sticks[i].position[5,0]) * drone.sticks[i].length/2,
        0,0,0,0])

        offset = np.reshape(offset,(6,1))

        node1 = drone.sticks[i].position + offset
        node2 = drone.sticks[i].position - offset

        drone.sticks[i].nodes = [Node(node1[0,0],node1[1,0]),Node(node2[0,0],node2[1,0])]
        print("working")
