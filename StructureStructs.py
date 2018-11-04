
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
        self.nodes = [node1,node2]

        self.node1 = np.array([node1.x,node1.y,node1.z])
        self.node2 = np.array([node2.x,node2.y,node2.z])
        self.cm = (self.node1 + self.node2)/2

        self.mass = 0.1
        # print(node1.x, node1.y, node1.z, node2.x, node2.y, node2.z)
        self.length = Distance(node1,node2)
        # print("Length ", self.length)
        self.intertia = (1/12) * self.mass * self.length**2
        self.mass = np.array([0.1, 0.1, 0.1, (1/12) * self.mass * self.length**2, 0, 0])
        self.mass = np.reshape(self.mass, (6,1))

        self.acceleration = np.zeros((6,1))
        self.velocity_vec = np.zeros((6,1))
        self.position = np.zeros((6,1))

        self.position[0:3,0] = (self.node1 + self.node2)/2
        delta = self.node1 - self.node2
        print(delta)
        self.position[5,0] = np.arctan2(delta[1],delta[0])


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
        self.p_connection = 1
        self.num_sticks = num_sticks
        self.sticks = dict()
        self.connections = dict()
        self.elastic_constant = 1
        self.initSticks(self.num_sticks)


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
                self.connections[i].append([c1,c2,stick_id])
                self.connections[stick_id].append([c2,c1,i])
