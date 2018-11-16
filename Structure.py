import numpy as np
from Element import Element
import copy

class Structure():
  uniqueId = 0
  def __init__(self, length = 0, numStruts = 0):
      # self.x_bounds = (-10,10)
      # self.y_bounds = (-10,10)
      # self.z_bounds = (-10,10)
      # self.alpha_bounds =
      # self.alpha_bounds =
      # self.alpha_bounds =
      self.mutated = False;
      self.uniqueId = Structure.uniqueId
      Structure.uniqueId += 1
      self.numStruts = numStruts
      self.num_nodes = numStruts * 2
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
      self.solved = False
      self.fitness = 0
  def duplicate(self):
      new = copy.deepcopy(self)
      new.uniqueId = Structure.uniqueId
      Structure.uniqueId += 1
      new.mutated = True
      return new
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
  def combine(self, mate):
      p_comb = np.random.rand()

      #Pad Nodes for Merge

      # NOT BEING USED RN B/C Sturctures are the same shape

      # Think about doing this for bc NODE shapes has changed now, will need to splice
      # in two places two do this properly
      new_num_nodes = int((self.num_nodes + mate.num_nodes)/2)
      if new_num_nodes % 2 != 0:
          new_num_nodes += 1

      new_num_struts = int(new_num_nodes/2)

      diff_mate = int(new_num_nodes - mate.num_nodes)
      diff_mate_strut = new_num_struts - mate.numStruts
      if (diff_mate >= 0):
          # pad to increase size
          mate_nodes = np.pad(mate.nodes,( (0,abs(diff_mate)),(0,0) ), mode='constant')
          mate_connections = np.pad(mate.C,( (0,abs(diff_mate)),(0,abs(diff_mate)) ), mode='constant')
      else:
          mate_nodes = mate.nodes[0:new_num_nodes,:]
          mate_connections = mate.C[0:new_num_nodes,0:new_num_nodes]

      diff_self = int(new_num_nodes - self.num_nodes)
      diff_self_strut = new_num_struts - self.numStruts

      if (diff_self >= 0):
          # pad to increase size
          self_nodes = np.pad(self.nodes,( (0,abs(diff_self)),(0,0) ), mode='constant')
          self_connections = np.pad(self.C,( (0,abs(diff_self)),(0,abs(diff_self)) ), mode='constant')

      else:
          self_nodes = self.nodes[0:new_num_nodes,:]
          self_connections = self.C[0:new_num_nodes,0:new_num_nodes]

      zero_base = new_num_nodes - max(diff_self, diff_mate)
      new_nodes = (self_nodes + mate_nodes)
      new_nodes[0:zero_base,:] /= 2

      zero_base_upper = new_num_struts - max(diff_mate_strut, diff_self_strut)
      zero_base_lower = 2*new_num_struts - max(diff_mate_strut, diff_self_strut)

      #mabye max this a max combine or a tit for tat in the future
      new_connections = (self_connections + mate_connections)

      new_connections[:int(zero_base_upper),:int(zero_base)] = new_connections[:int(zero_base_upper),:]/2
      new_connections[int(new_num_struts):int(zero_base_lower),:int(zero_base)] = new_connections[int(new_num_struts):int(zero_base_lower),:int(zero_base)]/2

      mask = np.random.rand(new_num_nodes,new_num_nodes)
      L = np.zeros((new_num_nodes,new_num_nodes))

      new_connections[new_connections >= mask] = 1
      L[new_connections >= mask] = 1
      new_connections
      # new_connections[new_num_struts:zero_base_lower,:] /= 2


      child = Structure(10,int(new_num_nodes/2))

      for i in np.arange(new_num_struts):
           new_connections[i,i+new_num_struts] = 0
           new_connections[i+new_num_struts,i] = 0
           L[i+new_num_struts,i] = 10
           L[i,i+new_num_struts] = 10

      new_connections[np.eye(self.numElements*2)==1] = 0
      L[np.eye(self.numElements*2)==1] = -1 #small number to avoid nans

      return p_comb
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

  def resetElements(self):
      for strut in self.elements:
          strut.randomPosition()

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

  def mutateC(self):
      self.C = self.C + np.random.normal(size=(self.num_nodes,self.num_nodes))

      self.C = self.C/2 + self.C.T/2

      mask1 = self.C<0.5
      mask2 = self.C>=0.5
      self.C[mask1] = 0
      self.L[mask1] = 0
      self.L[mask2] = 1 # intial wire length
      self.C[mask2] = 1 # Spring Constant
      mask3 = np.diag_indices(self.numElements*2)
      self.C[mask3] = 0
      self.L[mask3] = -1 #small number to avoid nans

      for i in np.arange(self.numElements):
          self.C[i,i+self.numElements] = 0
          self.C[i+self.numElements,i] = 0
          self.L[i+self.numElements,i] = self.length
          self.L[i,i+self.numElements] = self.length

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

       C = np.array([[0, 0, 0, 1],
       [0, 0, 0, 0],
       [0, 0, 0, 0],
       [1, 0, 0, 0]])

       # C = np.array([[0, 1, 1, 0, 1, 0],
       #               [1, 0, 1, 0, 0, 1],
       #               [1, 1, 0, 1, 0, 0],
       #               [0, 0, 1, 0, 1, 1],
       #               [1, 0, 0, 1, 0, 1],
       #               [0, 1, 0, 1, 1, 0]])

       C[C<0.5] = 0
       L[C>=0.5] = 5 # intial wire length
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
