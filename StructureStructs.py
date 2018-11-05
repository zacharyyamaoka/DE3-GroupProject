import numpy as np
import matplotlib.pyplot as plt
from TrigFunctions import *

class Node:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class Stick:
    def __init__(self, node1, node2):

        self.length = Distance(node1,node2)
        self.mass = 0.1
        self.intertia = (1/12) * self.mass * self.length**2
        self.mass = np.array([0.1, 0.1, 0.1, (1/12) * self.mass * self.length**2, 1, 1])
        self.mass = np.reshape(self.mass, (6,1))

        self.node1 = np.array([node1.x,node1.y,node1.z])
        self.node2 = np.array([node2.x,node2.y,node2.z])

        self.acceleration = np.zeros((6,1))
        self.velocity = np.zeros((6,1))
        self.position = np.zeros((6,1))
        self.net_force = np.zeros((6,1))
        self.total_force = np.zeros((6,1))

        self.position[0:3,0] = (self.node1 + self.node2)/2
        delta = self.node1 - self.node2
        self.position[5,0] = np.arctan2(delta[1],delta[0])

        offset = np.array([np.cos(self.position[5,0]) * self.length/2,
        np.sin(self.position[5,0]) * self.length/2,
        0,0,0,0])

        offset = np.reshape(offset,(6,1))
        node1 = self.position + offset
        node2 = self.position - offset

        self.nodes = [Node(node1[0,0],node1[1,0]),Node(node2[0,0],node2[1,0])]


class Structure:

    def __init__(self):

        # Constraints

        # can we begin to infleunce the shape
        self.symmetrix_y = True
        self.symmetrix_x = True

        self.max_weight = 0

    def combine(structure):
        return self

    def mutate():
        return self


class PaperDrone2D(Structure):

    def __init__(self, num_sticks):
        super().__init__()
        self.p_connection = 0.5
        self.num_sticks = num_sticks
        self.sticks = dict()
        self.connections = dict()
        self.elastic_constant = 1
        
        self.initSticks(self.num_sticks)
        self.net_force=0
        self.total_force=0
        self.check_force = np.zeros((6,1))

    def mutate(self):

        for i in np.arange(self.num_sticks):
            new_connections = []
            for connection in self.connections[i]:
                selector = np.random.rand(1)[0]
                selector = 0
                if selector < 0.33:


                    sample_connection = np.array([np.random.randint(1,3,1)[0], np.random.randint(1,3,1)[0], np.random.randint(0,self.num_sticks,1)[0]])

                    for i in range(3):
                        if (np.random.rand(1)[0] < 1):
                            connection[i] = sample_connection[i]
                    new_connections.append(connection)

                elif selector < 0.66:
                    pass

                else:
                    new_connections.append(connection)

            self.connections[i] = new_connections


    def combine(self, new_drone):
        combine_p = np.random.rand(1)[0]
        # combine_p = 1
        new_stick_dict = dict()
        keep_sticks = round(combine_p*self.num_sticks)
        new_sticks = round(new_drone.num_sticks * (1-combine_p))
        counter = 0
        pointer = 0

        new_connections = dict()
        new_total = keep_sticks+new_sticks
        for i in np.arange(new_total):
            new_connections[i] = []

        for i in np.arange(max(keep_sticks,new_sticks)):

            if counter < keep_sticks:
                new_stick_dict[pointer] = self.sticks[i]
                for connection in self.connections[i]:
                    if connection[2] < new_total:
                        new_connections[pointer].append(connection)
                        new_connections[connection[2]].append([connection[1],connection[0],pointer])
                pointer += 1

            if counter < new_sticks:

                ind = int(new_drone.num_sticks - i - 1)
                print(ind)
                new_stick_dict[pointer] = new_drone.sticks[ind]
                print("ADDING NEW STICK")
                for connection in new_drone.connections[ind]:
                    if connection[2] < new_total:
                        new_connections[pointer].append(connection)
                        new_connections[connection[2]].append([connection[1],connection[0],pointer])
                pointer += 1
            counter += 1

        print("Here")
        self.connections = new_connections
        self.num_sticks = new_total
        self.sticks = new_stick_dict
        #keep the first sticks in the dict

        return self

    def initSticks(self, num_sticks=0):
        self.sticks.clear()
        for i in np.arange(num_sticks):
            self.connections[i] = []

        for i in np.arange(num_sticks):
            rc = np.random.uniform(-10,10,4)
            self.sticks[i] = Stick(Node(rc[0],rc[1]),Node(rc[2],rc[3]))

            for k in np.arange(np.random.randint(1,num_sticks+1)): #pick a random number of sticks to consider
                stick_id = np.random.randint(0,num_sticks)

                if stick_id == i:
                    continue
                c1 = np.random.randint(1,3)
                c2 = np.random.randint(1,3)
                self.connections[i].append(np.array([c1,c2,stick_id]))
                self.connections[stick_id].append(np.array([c1,c2,stick_id]))
