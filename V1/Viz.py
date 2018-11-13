import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections  as mc

class Viz:
    """ Class for managing Vizulzation of drones"""
    def __init__(self, drones, rows, colums):
        self.drones = drones
        self.plots = dict()
        self.plot_i = 0
        self.plot_j = 0
        self.createGrid(rows, colums)


    def createGrid(self,row=10,col=10):

        self.rows = row
        self.colums= col
        self.plots.clear()
        self.plotId = dict()
        counter = 0

        plt.figure(0)
        for i in range(row):
            for j in range(col):
                ax = plt.subplot2grid((row,col), (i,j), projection='3d')
                self.plots[(i,j)] = ax
                self.plotId[counter] = (i,j)
                counter += 1
    def updateDrones(self, drones):
        self.drones = drones
    def showDrones(self, wait = 0.1):

        # create grid
        count = 0
        for drone in self.drones:
            # self.draw2Dsticks(drone,count)
            self.draw3DPaperDrone(drone,count)


            count += 1
            # self.draw2Dstrings(drone)

        plt.show()
        plt.pause(wait)

    def getPlotId(self, ind):
        total_plots = self.rows * self.colums
        return self.plotId[ind%total_plots]

    def getNewPlotId(self):

        id = (self.plot_i,self.plot_j)

        if self.plot_j < self.colums - 1:
            self.plot_j += 1

        else:
            self.plot_j = 0

            if self.plot_i < self.rows - 1:
                self.plot_i += 1

            else:
                self.plot_i = 0

        return id

    # def draw2Dstrings(self,drone):
    #     num_sticks = drone.num_sticks
    #     for i in np.arange(num_sticks):
    #

    def draw3DPaperDrone(self,drone,ind):
        drawn = {}
        lines = []
        line_colours = []
        strings = []
        string_colours = []

        if (ind > self.rows*self.colums):
            return

        nodeXY = drone.nodes[:,0:2]
        connections = drone.connections
        # rows = np.shape(connections)[0]
        # cols = np.shape(connections)[1]
        # print(connections)

        for i in np.arange(drone.num_nodes):
            row = connections[i]
            for j in np.arange(drone.num_nodes):
                connection = row[j]
                if connection == 1: #draw elastic
                    start = (nodeXY[i,0],nodeXY[i,1])
                    end = (nodeXY[j,0],nodeXY[j,1])
                    end_points = [start,end]
                    c = (0,0,1,0.8)
                    string_colours.append(c)
                    strings.append(end_points)

                if connection > 50: #draw bar
                    start = (nodeXY[i,0],nodeXY[i,1])
                    end = (nodeXY[j,0],nodeXY[j,1])
                    end_points = [start,end]
                    c = (0,0,0,0.5)
                    line_colours.append(c)
                    lines.append(end_points)

        string_lc = mc.LineCollection(strings, colors=string_colours, linewidths=1)
        lc = mc.LineCollection(lines, colors=line_colours, linewidths=3)
        # curr_ax = self.plots[self.getNewPlotId()]
        curr_ax = self.plots[self.getPlotId(ind)]
        colors = np.random.rand(4)
        curr_ax.cla()
        curr_ax.scatter(nodeXY[0:4,0],nodeXY[0:4,1],s=200, c="b", alpha = 0.3)
        curr_ax.scatter(nodeXY[:,0],nodeXY[:,1],s=10)

        curr_ax.add_collection(lc)
        curr_ax.add_collection(string_lc)
        # curr_ax.autoscale()
        curr_ax.set_xlim([-13,13])
        curr_ax.set_ylim([-13,13])
        curr_ax.axis('equal')
        curr_ax.set_yticklabels([])
        curr_ax.set_xticklabels([])
        curr_ax.margins(1)

    def draw2Dsticks(self,drone,ind):

        drawn = {}
        lines = []
        strings = []
        string_colours = []
        colours = []

        num_sticks = drone.num_sticks
        connections = drone.connections
        # rows = np.shape(connections)[0]
        # cols = np.shape(connections)[1]
        # print(connections)

        for i in np.arange(num_sticks):
            stick = drone.sticks[i]
            end_points = [(stick.nodes[0].x,stick.nodes[0].y),(stick.nodes[1].x,stick.nodes[1].y)]
            c = (1,0,0,1)
            colours.append(c)
            lines.append(end_points)
            # print(connections[i,:])
            for j in connections[i]:
                # print(j)
                end_id = int(j[2])
                c1 = int(j[0]) - 1
                c2 = int(j[1]) - 1
                print("end id:", end_id)
                print("num sticks:", num_sticks)
                end_stick = drone.sticks[end_id]
                start = (stick.nodes[c1].x,stick.nodes[c1].y)
                end = (end_stick.nodes[c2].x,end_stick.nodes[c2].y)

                end_points = [start,end]

                c = (0,0,1,1)
                string_colours.append(c)
                strings.append(end_points)


        string_lc = mc.LineCollection(strings, colors=string_colours, linewidths=1)
        lc = mc.LineCollection(lines, colors=colours, linewidths=2)
        # curr_ax = self.plots[self.getNewPlotId()]
        curr_ax = self.plots[self.getPlotId(ind)]

        curr_ax.cla()
        curr_ax.add_collection(lc)
        curr_ax.add_collection(string_lc)
        # curr_ax.autoscale()
        curr_ax.set_xlim([-10,10])
        curr_ax.set_ylim([-10,10])
        curr_ax.margins(0.1)
