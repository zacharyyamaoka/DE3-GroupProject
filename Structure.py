import numpy as np
from Element import Element

class Structure():
  def __init__(self, length = 0, numStruts = 0):
      # self.x_bounds = (-10,10)
      # self.y_bounds = (-10,10)
      # self.z_bounds = (-10,10)
      # self.alpha_bounds =
      # self.alpha_bounds =
      # self.alpha_bounds =
      self.numStruts = numStruts
      self.initStruts(numStruts, length)
      self.initNodes(self.elements)
      self.initConnections()
      self.D = np.zeros((numStruts*2,numStruts*2))
      pass

  def initStruts(self, numStruts, length):
      self.elements = []
      self.numElements = numStruts
      for i in np.arange(numStruts):
           self.elements.append(Element(length=length, random=True))
          #Create a strut of given length in a random location
  def initNodes(self, elements):
      numStruts = len(elements)
      self.nodes = np.zeros((numStruts*2,3))

      for i in np.arange(numStruts):

          self.nodes[i,:] = elements[i].getNodePosition(1).T
          self.nodes[i + numStruts,:] = elements[i].getNodePosition(2).T

  def initConnections(self):

       C = np.random.rand(self.numElements*2,self.numElements*2)

       #ensure symmetry
       C = C/2 + C.T/2
       C[C>=0.5] = 1
       C[C<0.5] = 0
       C[np.eye(self.numElements*2)==1] = 0

       for i in np.arange(self.numElements):
           C[i,i+self.numElements] = 2
           C[i+self.numElements,i] = 2

       self.C = C
