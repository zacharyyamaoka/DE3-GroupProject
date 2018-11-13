import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

class Vizulization():
  def __init__(self):
      pass

  def show(self, structure):
      fig = plt.figure()
      ax = plt.axes(projection='3d')
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

      plt.show()
