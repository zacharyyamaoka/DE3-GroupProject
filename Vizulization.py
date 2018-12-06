import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Vizulization():
  def __init__(self,rows=1,cols=1):
      self.on = False
      self.drone_figure = 0
      self.graph = []
      self.figures_list = []
      self.figures = 0
      self.createGrid(rows,cols)
      self.struts = 0
  def setStruts(self, num):
      self.struts= num
  def getFigureId(self):
      id = self.figures
      self.figures += 1
      return id

  def getPlotId(self, ind):
      total_plots = self.rows * self.colums
      return self.plotId[ind%total_plots]

  def createGraph(self):
      fig = plt.figure(self.getFigureId())
      self.figures_list.append(fig)
      ax1 = fig.add_subplot(1, 1, 1)
      self.graph.append(ax1)
      return len(self.graph)
  def clearGraph(self,ind):
      ax = self.graph[ind-1]
      ax.cla()
  def plotGraph(self,ind,x,y,c='black'):
      ax = self.graph[ind-1]
      ax.scatter([y],[x],color=c)
      pass
  def legendGraph(self,ind,label="",c="black"):
      ax = self.graph[ind-1]
      red_patch = mpatches.Patch(color=c, label=label)
      ax.legend(handles=[red_patch])

  def labelGraph(self,ind,title="",xaxis="",yaxis=""):
      ax = self.graph[ind-1]
      ax.set_title(title)

  def createGrid(self,row=2,col=2):

      self.rows = row
      self.colums= col
      self.plotId = dict()
      self.plots = dict()
      counter = 0

      fig = plt.figure(self.getFigureId())
      self.figures_list.append(fig)
      for i in range(row):
          for j in range(col):
              ax = plt.subplot2grid((row,col), (i,j), projection='3d')
              ax.grid(False)
              ax.set_yticklabels([])
              ax.set_xticklabels([])
              ax.set_zticklabels([])
              ax.autoscale(False)

              # ax.margins(0.1)
              self.plots[(i,j)] = ax
              self.plotId[counter] = (i,j)
              counter += 1

  def init(self):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

  def F(self, structure, hold_on = False):
     ax = self.plots[self.getPlotId(1)]
     ax.cla()

     num = structure.numElements*2

     #Draw Struts
     for i in np.arange(structure.numElements):
         rows = np.array([i,i+structure.numElements])
         ax.plot3D(structure.nodes[rows,np.array([0,0])], structure.nodes[rows,np.array([1,1])], structure.nodes[rows,np.array([2,2])], 'black',linewidth=3)

     Fmat = structure.F #+ nodes
     for i in np.arange(1):
         row = Fmat[i]
         for j in np.arange(num):
             if j != i:
                     start = structure.nodes[i]
                     end = row[j]
                     if np.sum(end) != 0:
                         ax.quiver(start[0], start[1], start[2], end[0], end[1], end[2], normalize = False)
                         ax.scatter3D(start[0], start[1], start[2]);

  def D(self, structure, hold_on = False):
      # if not self.on:
      #     self.on = True
      #     self.init()
      ax = self.plots[self.getPlotId(ind)]

      ax = plt.axes(projection='3d')

      num = structure.numElements*2

      #Draw Struts
      for i in np.arange(structure.numElements):
          rows = np.array([i,i+structure.numElements])
          ax.plot3D(structure.nodes[rows,np.array([0,0])], structure.nodes[rows,np.array([1,1])], structure.nodes[rows,np.array([2,2])], 'black',linewidth=3)

      # Draw Displacement Vectors
      # nodes = structure.nodes.reshape(structure.numElements*2,1,3)
      # nodes = np.tile(nodes,(1,num,1))

      D_back = structure.D #+ nodes
      for i in np.arange(num):
          row = D_back[i]
          for j in np.arange(num):
              if j != i:
                  start = structure.nodes[i]
                  end = row[j]
                  v = np.array([start,end])
                  ax.quiver(start[0], start[1], start[2], end[0], end[1], end[2], normalize = False)

                  # ax.plot3D(v[:,0], v[:,1], v[:,2], 'red')

      if not hold_on:
          plt.show()
  def saveFigs(self):
      for i in range(len(self.figures_list)):
        self.figures_list[i].savefig('bar_%d_fig_%d' %(self.struts,i))
  def show(self, structure, ind, hold_on = False):

      ax = self.plots[self.getPlotId(ind)]
      ax.cla()

      ax.text2D(0.05, 0.95, 'ID: %d Fit: %0.3f' % (structure.uniqueId, structure.fitness), transform=ax.transAxes)

      num = structure.numElements
      for i in np.arange(num):
          rows = np.array([i,i+num])
          ax.plot3D(structure.nodes[rows,np.array([0,0])], structure.nodes[rows,np.array([1,1])], structure.nodes[rows,np.array([2,2])], 'black',linewidth=4)

      for i in np.arange(num*2):
          row = structure.C[i]
          for j in np.arange(num*2):
              if row[j] == 1:
                  rows = np.array([i,j])
                  if structure.Delta[i,j] == 0:
                      colour = 'blue'
                  else:
                      colour = 'red'
                  ax.plot3D(structure.nodes[rows,np.array([0,0])], structure.nodes[rows,np.array([1,1])], structure.nodes[rows,np.array([2,2])],c=colour)

      ax.scatter3D(structure.nodes[:,0], structure.nodes[:,1], structure.nodes[:,2], c="b");
      X = np.arange(-10,10)
      Y = np.arange(-10,10)
      Z = np.arange(-10,10)

      max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
      Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
      Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
      Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
      for xb, yb, zb in zip(Xb, Yb, Zb):
          ax.plot([xb], [yb], [zb], 'w')
      ax.set_xlim([-10,10])
      ax.set_ylim([-10,10])
      ax.set_zlim([-10,10])
      ax.set_yticklabels([])
      ax.set_xticklabels([])
      ax.set_zticklabels([])
      # ax.set_aspect(1)
      ax.set_aspect('equal')
