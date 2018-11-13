import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

class Vizulization():
  def __init__(self):
      pass
      self.on = False

  def init(self):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

  def D(self, structure, hold_on = False):
      # if not self.on:
      #     self.on = True
      #     self.init()
      fig = plt.figure()
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

  def show(self, structure, hold_on = False):

      if not self.on:
          self.on = True
          self.init()

      num = structure.numElements
      for i in np.arange(num):
          rows = np.array([i,i+num])
          ax.plot3D(structure.nodes[rows,np.array([0,0])], structure.nodes[rows,np.array([1,1])], structure.nodes[rows,np.array([2,2])], 'black')

      for i in np.arange(num*2):
          row = structure.C[i]
          for j in np.arange(num*2):
              if row[j] == 1:
                  rows = np.array([i,j])
                  ax.plot3D(structure.nodes[rows,np.array([0,0])], structure.nodes[rows,np.array([1,1])], structure.nodes[rows,np.array([2,2])], 'red')

      ax.scatter3D(structure.nodes[:,0], structure.nodes[:,1], structure.nodes[:,2], c=structure.nodes[:,2], cmap='Greens');

      if not hold_on:
          plt.show()
