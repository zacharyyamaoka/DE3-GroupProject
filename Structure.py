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
      self.F = np.zeros((numStruts*2,numStruts*2))
      self.modified_elements = [] #careful for memory?
      self.old_D = []
      self.old_F = []
      self.max_element = 0
      self.max_force = 0
      self.E_total = 0
      self.old_Nodes = 0
      self.F_total = np.zeros(numStruts)

  def setD(self, new_D):
      self.old_D.append(self.D)
      self.D = new_D

  def setF(self, new_F):
      self.old_F.append(self.F)
      self.F = new_F

  def revertElemement(self, ind):
      self.elements[ind].revertPosition()

  def revertStructure(self):
      self.nodes = self.old_Nodes
      # self.D = self.old_D.pop()
      # self.F = self.old_F.pop()
      # self.elements[self.modified_elements.pop()].revertPosition()

  def vibrate(self, elementInd, multipler=0.01):
      # Can I estimate the optimal movement online
      x = np.random.uniform(-1,1)*multipler
      y = np.random.uniform(-1,1)*multipler
      z = np.random.uniform(-1,1)*multipler
      alpha = np.random.uniform(-3.14,3.14)*multipler
      beta = np.random.uniform(-3.14,3.14)*multipler
      gamma = np.random.uniform(-3.14,3.14)*multipler

      self.modified_elements.append(elementInd)
      self.elements[elementInd].wiggle(x,y,z,alpha,gamma,beta)

  def initStruts(self, numStruts, length):
      self.elements = []
      self.numElements = numStruts
      self.numStruts = numStruts
      self.length = length
      for i in np.arange(numStruts):
           self.elements.append(Element(length=length, random=True))
          #Create a strut of given length in a random location
  def initNodes(self, elements):
      numStruts = len(elements)
      self.nodes = np.zeros((numStruts*2,3))

      for i in np.arange(numStruts):

          self.nodes[i,:] = elements[i].getNodePosition(1).T
          self.nodes[i + numStruts,:] = elements[i].getNodePosition(2).T

  def refresh(self):
      self.old_Nodes = self.nodes
      self.initNodes(self.elements)

  def updateElementNodes(self,ind):
      self.nodes[ind,:] = self.elements[ind].getNodePosition(1).T
      self.nodes[ind + self.numStruts,:] = self.elements[ind].getNodePosition(2).T

  def initConnections(self):

       C = np.random.rand(self.numElements*2,self.numElements*2)
       L = np.zeros((self.numElements*2,self.numElements*2))
       #ensure symmetry
       C = C/2 + C.T/2

       # Plant in a spy
       # C = np.array([[0, 1, 0, 1],
       # [1, 0, 1, 0],
       # [0, 1, 0, 1],
       # [1, 0, 1, 0]])

       C = np.array([[0, 1, 1, 0, 1, 0],
                     [1, 0, 1, 0, 0, 1],
                     [1, 1, 0, 1, 0, 0],
                     [0, 0, 1, 0, 1, 1],
                     [1, 0, 0, 1, 0, 1],
                     [0, 1, 0, 1, 1, 0]])

       C[C<0.5] = 0
       L[C>=0.5] = 1 # intial wire length
       C[C>=0.5] = 1 # Spring Constant

       C[np.eye(self.numElements*2)==1] = 0
       L[np.eye(self.numElements*2)==1] = -1 #small number to avoid nans

       for i in np.arange(self.numElements):
           C[i,i+self.numElements] = 0
           C[i+self.numElements,i] = 0
           L[i+self.numElements,i] = self.length
           L[i,i+self.numElements] = self.length

       self.L = L
       self.C = C
