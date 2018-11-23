import numpy as np
from Element import Element
import copy

class Structure():
  uniqueId = 0
  def __init__(self, length = 0, numStruts = 0, init = True):
      # self.x_bounds = (-10,10)
      # self.y_bounds = (-10,10)
      # self.z_bounds = (-10,10)
      # self.alpha_bounds =
      # self.alpha_bounds =
      # self.alpha_bounds =
      self.mutated = False
      self.uniqueId = Structure.uniqueId
      Structure.uniqueId += 1
      self.numStruts = numStruts
      self.num_nodes = numStruts * 2

      if init:
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
      # new.mutated = True
      return new
  def setD(self, new_D):
      self.old_D.append(self.D)
      self.D = new_D

  def setF(self, new_F):
      self.old_F.append(self.F)
      self.F = new_F

  def revertElemement(self, ind):
      self.elements[ind].revertPosition()
  def mimic(self, mate):
      self.L = np.copy(mate.L)
      self.C = np.copy(mate.C)
      self.nodes = np.copy(mate.nodes)
      self.elements = np.copy(mate.elements)
      # self.nodes[:,:] = 0
  def revertStructure(self):
      self.nodes = self.old_Nodes
      # self.D = self.old_D.pop()
      # self.F = self.old_F.pop()
      # self.elements[self.modified_elements.pop()].revertPosition()

  def getCombineElement(self, ind, mateMax, selfMax, mateElements, selfElements):

      if (ind > mateMax) or (ind > selfMax):
          if mateMax > selfMax:
              return mateElements[ind]
          else:
              return selfElements[ind]

      switch = (ind%2 == 0)

      if switch:
        return mateElements[ind]

      else:
          return selfElements[ind]


  def combine(self, mate, ratio=np.random.rand()):
      #Pick Combine Ratio
      p_comb = ratio
      child = self.duplicate()

      # Re-initalize class parameters
      p_self = 1 - p_comb
      p_mate = p_comb
      element_self = int(np.ceil(p_self*self.numStruts))
      element_mate = int(np.floor(p_mate*mate.numStruts))

      new_num_elements = element_self + element_mate
      new_num_nodes = new_num_elements * 2

      mate_num_nodes = element_mate * 2
      self_num_nodes = element_self * 2

      child = self.duplicate()
      child.C = np.zeros((new_num_nodes,new_num_nodes))
      child.nodes = np.zeros((new_num_nodes,3))

      child.numStruts = new_num_elements
      child.num_nodes = new_num_nodes
      child.numElements = new_num_elements

      # Update Elements with cross over
      if self.numStruts < mate.numStruts: #element self first
        new_elements = child.elements[0:element_self]
        new_elements.extend(mate.elements[element_self:element_self+element_mate])

      else: #element mate first
        new_elements = mate.elements[0:element_mate]
        new_elements.extend(self.elements[element_mate:element_self+element_mate])

      child.elements = new_elements

      p_element = np.random.rand()

      diff_mate = int(new_num_nodes - mate.num_nodes)

      # determine Hotzone
      ind = np.minimum(element_self, element_mate)
      hotzone_upper = (ind,ind*2)
      hotzone_lower = (new_num_elements+ind,ind*2)

      if (element_self < element_mate):
          hotMat = self.C
          coldMat = mate.C
      else:
          hotMat = mate.C
          coldMat = self.C


      if (diff_mate >= 0):

          child.C[0:mate.numStruts,0:mate.num_nodes] += p_mate * mate.C[0:mate.numStruts,0:mate.num_nodes]
          child.C[new_num_elements:new_num_elements+mate.numStruts,0:mate.num_nodes] += p_mate * mate.C[mate.numStruts:mate.numStruts+mate.numStruts,0:mate.num_nodes]

      else:
          #Other wise your bigger, this part just needs some consideration
          child.C[0:self.numStruts,0:self.num_nodes] \
          += p_mate * mate.C[0:self.numStruts,0:self.num_nodes]
          child.C[new_num_elements:new_num_elements+self.numStruts,0:self.num_nodes] \
          += p_mate * mate.C[self.numStruts:self.numStruts+self.numStruts,0:self.num_nodes]

          child.C[self.numStruts:new_num_elements,self.num_nodes:new_num_nodes] \
          += mate.C[self.numStruts:new_num_elements,self.num_nodes:new_num_nodes]

          child.C[new_num_elements+self.numStruts:new_num_elements+new_num_elements,self.num_nodes:new_num_nodes] \
          += mate.C[new_num_elements+self.numStruts:new_num_elements+new_num_elements,self.num_nodes:new_num_nodes]

      diff_self = int(new_num_nodes - self.num_nodes)

      if (diff_self >= 0):

          child.C[0:self.numStruts,0:self.num_nodes] +=  p_self *self.C[0:self.numStruts,0:self.num_nodes]
          child.C[new_num_elements:new_num_elements+self.numStruts,0:self.num_nodes] += p_self * self.C[self.numStruts:self.numStruts+self.numStruts,0:self.num_nodes]

      else:

          child.C[0:mate.numStruts,0:mate.num_nodes] \
          += p_self * self.C[0:mate.numStruts,0:mate.num_nodes]
          
          child.C[new_num_elements:new_num_elements+mate.numStruts,0:mate.num_nodes] \
          += p_self * self.C[mate.numStruts:mate.numStruts+mate.numStruts,0:mate.num_nodes]

          child.C[mate.numStruts:new_num_elements,mate.num_nodes:new_num_nodes] \
          += self.C[mate.numStruts:new_num_elements,mate.num_nodes:new_num_nodes]

          child.C[new_num_elements+mate.numStruts:new_num_elements+new_num_elements,mate.num_nodes:new_num_nodes] \
          += self.C[new_num_elements+mate.numStruts:new_num_elements+new_num_elements,mate.num_nodes:new_num_nodes]

      # print("---------- NODES ------------")
      # print(child.nodes)
      # print(self.nodes)
      # print(mate.nodes)

      zero_base_strut =  np.minimum(element_self, element_mate)
      zero_base_node = zero_base_strut*2
      print("zero_base_strut: ",zero_base_strut)
      print(child.C)
      child.C[0:zero_base_strut,0:zero_base_node] /= 2
      print(child.C)
      child.C[new_num_elements:new_num_elements+zero_base_strut,0:zero_base_node] /= 2
      print(child.C)
      print("------------C-------------- ^^")
      mask = np.random.rand(new_num_nodes,new_num_nodes)
      child.L = np.zeros((new_num_nodes,new_num_nodes))

      mask1 = child.C >= mask
      child.C[mask1] = 1 #Elasticity of Connection
      child.C[np.logical_not(mask1)] = 0
      child.L[mask1] = 5 #string connections
      for i in np.arange(child.numStruts):
          child.C[i,i+child.numStruts] = 0
          child.C[i+child.numStruts,i] = 0
          child.L[i+child.numStruts,i] = child.length
          child.L[i,i+child.numStruts] = child.length

      # Apply Changes to Object
      child.refresh()
      return child

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
       #
       # C = np.array([[0, 0, 0, 1],
       # [0, 0, 0, 0],
       # [0, 0, 0, 0],
       # [1, 0, 0, 0]])

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
       L[np.eye(self.numElements*2)==1] = 0 #small number to avoid nans

       for i in np.arange(self.numElements):
           C[i,i+self.numElements] = 0
           C[i+self.numElements,i] = 0
           L[i+self.numElements,i] = self.length
           L[i,i+self.numElements] = self.length

       self.L = L
       self.C = C
