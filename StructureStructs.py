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

class PaperDrone3D(Structure):
    def __init__(self, num_nodes):
        super().__init__()

        if num_nodes % 2 != 0:
            num_nodes += 1

        self.p_connection = 0.5
        self.constraint_points = 4
        self.constraint_matrix = [[10, 10, 0],[10, -10, 0],[-10, 10, 0],[-10, -10, 0]]

        self.elastic_constant = 1
        self.net_force=0
        self.total_force=0
        self.check_force = np.zeros((6,1))

        self.num_nodes = num_nodes + self.constraint_points #total num nodes
        self.num_sticks = self.num_nodes/2

        self.initDroneStructure(self.num_nodes)

    def initDroneStructure(self, num_nodes):
        nodes = np.random.uniform(-10,10,(num_nodes,3))
        nodes[0:self.constraint_points,:] = self.constraint_matrix
        nodes[:,2] = 0
        connections = np.zeros((num_nodes,num_nodes))
        mask = np.random.rand(num_nodes,num_nodes) < self.p_connection/2
        connections[mask] = 1
        connections += connections.T
        connections[connections > 0] = 1
        connections[np.eye(num_nodes)==1] = 0 #makes sure that you don't connect to yourself

        basket = np.arange(num_nodes)
        pick_basket = np.arange(num_nodes)
        basket_len = num_nodes
        while (basket_len != 0):
            i = pick_basket[0]
            pick_basket = np.delete(pick_basket,0)
            basket_len -= 1

            ind = np.random.randint(0,basket_len)
            print(pick_basket)
            j = pick_basket[ind]
            if (np.size(pick_basket) > 1):
                pick_basket = np.delete(pick_basket,ind)
            basket_len -= 1

            print(pick_basket)
            print(i,j)
            connections[i,j] = 100
            connections[j,i] = 100
            print(connections)
            print(basket_len)

        self.nodes = nodes
        self.connections = connections
        print("Init")
        print(connections)
        #set Z to zero
    def combine(self, mate):
        print("COMBINE")

        #Combine Structure
        new_num_nodes = int((self.num_nodes + mate.num_nodes)/2)

        if new_num_nodes % 2 != 0:
            new_num_nodes += 1

        diff_mate = int(new_num_nodes - mate.num_nodes)

        if (diff_mate >= 0):
            # pad to increase size
            mate_nodes = np.pad(mate.nodes,( (0,abs(diff_mate)),(0,0) ), mode='constant')
            mate_connections = np.pad(mate.connections,( (0,abs(diff_mate)),(0,abs(diff_mate)) ), mode='constant')
        else:
            mate_nodes = mate.nodes[0:new_num_nodes,:]
            mate_connections = mate.connections[0:new_num_nodes,0:new_num_nodes]

        diff_self = int(new_num_nodes - self.num_nodes)

        if (diff_self >= 0):
            # pad to increase size
            self_nodes = np.pad(self.nodes,( (0,abs(diff_self)),(0,0) ), mode='constant')
            self_connections = np.pad(self.connections,( (0,abs(diff_self)),(0,abs(diff_self)) ), mode='constant')

        else:
            self_nodes = self.nodes[0:new_num_nodes,:]
            self_connections = self.connections[0:new_num_nodes,0:new_num_nodes]

        # new_nodes =
        print(new_num_nodes)
        print("Connections")
        print("SELF")

        print(self_nodes)
        print(self_connections)
        print("MATE")

        print(mate_nodes)
        print(mate_connections)
        #don't average zero, that has no meaning
        new_nodes = (self_nodes + mate_nodes)
        new_nodes[(self_nodes != 0) & (mate_nodes != 0)] /= 2
        zero_base = new_num_nodes - max(diff_self, diff_mate)
        new_nodes[self.constraint_points:zero_base,:] /= 2
        self.nodes = new_nodes

        #Combine connections
        new_connections = (self_connections + mate_connections)
        new_connections[0:zero_base,0:zero_base] /= 2
        mask = np.random.rand(new_num_nodes,new_num_nodes)

        # Look into altering this later
        new_connections[new_connections < mask] = 0


        beam_mask = np.max(new_connections, axis = 1) != 100
        beam_basket = np.arange(new_num_nodes)[beam_mask]
        beam_basket_len = np.size(beam_basket)

        for i in beam_basket:
            print("Beam Basket")
            inds = np.nonzero(new_connections[i] >= 50)[0]

            selector = np.random.randint(0,2,1)[0]
            print(inds)
            print(selector)
            j = inds[selector]
            inds = np.delete(inds,selector)
            new_connections[i,j] = 100
            new_connections[i,j] = 100

            j_dagger = inds[0]
            new_connections[i,j] = 0
            new_connections[i,j] = 0

        # while (beam_basket_len != 0):
        #     i = beam_basket[0]
        #     beam_basket = np.delete(beam_basket,0)
        #     beam_basket_len -= 1
        #
        #     ind = np.random.randint(0,beam_basket_len)
        #     print(pick_basket)
        #     j = pick_basket[ind]
        #     if (np.size(beam_basket) > 1):
        #         beam_basket = np.delete(beam_basket,ind)
        #     beam_basket_len -= 1
        #
        #     new_connections[i,j] = 100
        #     new_connections[j,i] = 100

        print("NEW")
        print(beam_basket)
        print(new_connections)
        print(beam_mask)


    def mutate(self):
        # adjust node positions
        noise = np.random.normal(0,1,(self.num_nodes,3))
        noise[0:self.constraint_points,:] = 0 # don't move constraint points
        noise[:,2] = 0 # no Noise in y
        # CAREFUL CHEKC THIS LINE ABOVE
        # self.nodes += noise
        count = np.sum(self.connections[self.connections == 1])/2
        print("Connections Before: ", count)
        #switch up connections of elastics
        noise2 = np.random.normal(0,1,(self.num_nodes,self.num_nodes))
        noise_connections = self.connections + noise2
        new_connections = self.connections

        lowerThresh = noise_connections < 0.5
        upperThresh = noise_connections > 0.5
        maxThresh = noise_connections > 50

        new_connections[((upperThresh) | (upperThresh.T)) & (self.connections==0)] = 1 #where both are connected then I SWITCH connection
        new_connections[((lowerThresh) | (lowerThresh.T)) & (self.connections==1)] = 0 #where both are connected then I SWITCH connection

        self.connections = new_connections

        count = np.sum(self.connections[self.connections == 1])/2
        print("Connections After: ", count)

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
                new_stick_dict[pointer] = new_drone.sticks[ind]
                for connection in new_drone.connections[ind]:
                    if connection[2] < new_total:
                        new_connections[pointer].append(connection)
                        new_connections[connection[2]].append([connection[1],connection[0],pointer])
                pointer += 1
            counter += 1

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
