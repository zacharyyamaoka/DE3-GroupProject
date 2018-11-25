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
      self.k = 5
      if init:
          self.initStruts(numStruts, length)
          self.initNodes(self.elements)
          self.initConnections()

      self.D = np.zeros((numStruts*2,numStruts*2))
      self.F = np.zeros((numStruts*2,numStruts*2))
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



      # Mutation Information
      self.wire_mutate_step = 1
      self.strut_mutate_step = 1
      self.connection_mutate_scale = 1
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
      child.L = np.zeros((new_num_nodes,new_num_nodes))
      # child.nodes = np.zeros((new_num_nodes,3))

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

      p_mate_L = np.random.rand(new_num_nodes,new_num_nodes)
      p_mate_L = np.ones((new_num_nodes,new_num_nodes)) * p_mate
      p_mate_L[mate.L==0] = 0
      p_mate_L[self.L==0] = 1
      p_self_L = -p_mate_L + 1

      new_C = p_mate*mate.C + p_self * self.C
      new_L = p_mate_L*mate.L + p_self_L * self.L

      mask = np.random.rand(new_num_nodes,new_num_nodes)

      new_connection = new_C >= mask
      new_length = np.copy(new_connection)
      child.C[new_connection] = 1 #Elasticity of Connection

      zero = new_L == 0

      for i in np.arange(self.numElements): #ensure valid C
          child.elements[i].length = new_L[i,i+self.numElements]
          new_length[i,i+self.numElements] = True #don't connect to you self
          new_length[i+self.numElements,i] = True
      child.L[new_length] = new_L[new_length]

      child.refresh()
      return child

  def vibrate(self, elementInd, type, multipler=0.01):
      # Can I estimate the optimal movement online
      if type == 'move':
          x = np.random.uniform(-1,1)*multipler
          y = np.random.uniform(-1,1)*multipler
          z = np.random.uniform(-1,1)*multipler
          alpha = 0
          beta = 0
          gamma = 0
      if type == 'rotate':
          x = 0
          y = 0
          z = 0
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
           self.elements.append(Element(length=np.random.uniform(length), random=True))
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
  def mutateL(self):
      selector = self.C == 1 # where you have a elastic connection
      large_mutator = np.random.normal(scale = self.wire_mutate_step, size=(self.num_nodes,self.num_nodes))
      large_mutator = (large_mutator + large_mutator.T)/2 #ensure symmetry
      self.L[selector] += large_mutator[selector]
      # self.C = self.C + np.random.normal(size=(self.num_nodes,self.num_nodes))
      for i in np.arange(self.numElements): # mutate the bar lengths by some amount aswell
          mutation = np.random.normal(scale = self.strut_mutate_step)
          self.L[i+self.numElements,i] += mutation
          self.L[i,i+self.numElements] += mutation
          self.elements[i].mutateLength(mutation)
      self.L = np.abs(self.L) # ensure lengths remain postive
  def mutateC(self):
      self.C = self.C + np.random.normal(scale = self.connection_mutate_scale, size=(self.num_nodes,self.num_nodes))
      self.C = (self.C + self.C.T)/2

      new_C = np.zeros((self.num_nodes,self.num_nodes))
      # new_L = np.zeros((self.num_nodes,self.num_nodes))
      for i in np.arange(self.numElements): #ensure valid C
          self.C[i,i] = 0
          self.C[i,i+self.numElements] = 0 #don't connect to you self
          self.C[i+self.numElements,i] = 0

      remove_connection = self.C<0.5
      new_connection = self.C>=0.5
      remove_length = np.copy(remove_connection)
      for i in np.arange(self.numElements): #ensure valid C
          remove_length[i,i+self.numElements] = False #don't connect to you self
          remove_length[i+self.numElements,i] = False

      zero = self.L == 0

      self.L[remove_length] = 0

      self.L[(new_connection) & (zero)] = \
      np.random.uniform(0,self.length,size=(self.num_nodes,self.num_nodes))[(new_connection) & (zero)]  # Reinitalize with random resting length

      new_C[new_connection] = 1
      self.C = new_C
      # for i in np.arange(self.numElements):
      #     self.C[i,i+self.numElements] = 0
      #     self.C[i+self.numElements,i] = 0
          # self.L[i+self.numElements,i] = self.length
          # self.L[i,i+self.numElements] = self.length
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

       # C = np.array([[0, 1, 0, 0],
       #             [1, 0, 1, 0],
       #             [0, 1, 0, 1],
       #             [0, 0, 1, 0]])
       new_connection = C>=0.5
       C[C<0.5] = 0
       L[new_connection] = 4 # intial wire length
       C[new_connection] = 1 # Spring Constant

       for i in np.arange(self.numElements):
           C[i,i] = 0
           C[i,i+self.numElements] = 0
           C[i+self.numElements,i] = 0
           L[i,i] = 0
           L[i+self.numElements,i] = self.elements[i].length
           L[i,i+self.numElements] = self.elements[i].length

       self.L = L
       self.C = C
