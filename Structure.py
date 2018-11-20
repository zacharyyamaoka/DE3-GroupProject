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
  def combine(self, mate):
      p_comb = np.random.rand()
      child = self.duplicate()

      element_self = int(p_comb*self.num_nodes)
      element_mate = int((1-p_comb)*mate.num_nodes)

      new_num_nodes = element_self + element_mate
      # new_num_nodes = int((self.num_nodes + mate.num_nodes)/2)

      if new_num_nodes % 2 != 0:
          new_num_nodes += 1

      new_num_nodes += 0
      new_num_struts = int(new_num_nodes/2)

      child = self.duplicate()
      child.C = np.zeros((new_num_nodes,new_num_nodes))
      child.nodes = np.zeros((new_num_nodes,3))

      p_node_self = np.random.rand(new_num_nodes,3)
      p_node_mate = np.ones((new_num_nodes,3)) - p_node_self
      # print("------MASK--------")
      # print(p_node_self)
      # print(p_node_mate)
      child.numStruts = new_num_struts
      child.num_nodes = new_num_nodes
      child.numElements = new_num_struts
      child.elements = []

      # don't do node operations

      # for i in np.arange(new_num_nodes):
      #     if i < element_self:
      #         pass
      #     if i < element_mate:
      #         pass

      p_element = np.random.rand()


      diff_mate = int(new_num_nodes - mate.num_nodes)
      diff_mate_strut = new_num_struts - mate.numStruts


      if (diff_mate >= 0):
          # pad to increase size
          child.nodes[0:mate.numStruts,:] += mate.nodes[0:mate.numStruts,:] *  p_node_mate[0:mate.numStruts,:]#1 * np.ones((mate.numStruts,3))
          child.nodes[new_num_struts:new_num_struts+mate.numStruts,:] += mate.nodes[mate.numStruts:mate.numStruts+mate.numStruts,:] * p_node_mate[new_num_struts:new_num_struts+mate.numStruts,:]#1 * np.ones((mate.numStruts,3))

          # # Weighted sum
          # nodes_new[0:mate.numStruts,:] *= 0.5 * np.ones((mate.numStruts,3)) #np.random.uniform(size=(mate.numStruts,3))
          # nodes_new[new_num_struts:new_num_struts+mate.numStruts,:] *= 0.5 * np.ones((mate.numStruts,3)) #np.random.uniform(size=(mate.numStruts,3))

          child.C[0:mate.numStruts,0:mate.num_nodes] += mate.C[0:mate.numStruts,0:mate.num_nodes]
          child.C[new_num_struts:new_num_struts+mate.numStruts,0:mate.num_nodes] += mate.C[mate.numStruts:mate.numStruts+mate.numStruts,0:mate.num_nodes]

      else:
          child.nodes[0:new_num_struts,:] += mate.nodes[0:new_num_struts,:] * p_node_mate[0:new_num_struts,:]# 1 * np.ones((new_num_struts,3))
          child.nodes[new_num_struts:new_num_struts+new_num_struts,:] += mate.nodes[mate.numStruts:mate.numStruts+new_num_struts,:] * p_node_mate[new_num_struts:new_num_struts+new_num_struts,:]# 1 * np.ones((new_num_struts,3))

          child.C[0:new_num_struts,0:new_num_nodes] += mate.C[0:new_num_struts,0:new_num_nodes]
          child.C[new_num_struts:new_num_struts+new_num_struts,0:mate.num_nodes] += mate.C[mate.numStruts:mate.numStruts+new_num_struts,0:new_num_nodes]

      diff_self = int(new_num_nodes - self.num_nodes)
      diff_self_strut = new_num_struts - self.numStruts
      if (diff_self >= 0):
          # pad to increase size
          child.nodes[0:self.numStruts,:] += self.nodes[0:self.numStruts,:] * p_node_self[0:self.numStruts,:]
          child.nodes[new_num_struts:new_num_struts+self.numStruts,:] += self.nodes[self.numStruts:self.numStruts+self.numStruts,:] * p_node_self[new_num_struts:new_num_struts+self.numStruts,:]

          # # Weighted sum
          # nodes_new[0:mate.numStruts,:] *= 0.5 * np.ones((mate.numStruts,3)) #np.random.uniform(size=(mate.numStruts,3))
          # nodes_new[new_num_struts:new_num_struts+mate.numStruts,:] *= 0.5 * np.ones((mate.numStruts,3)) #np.random.uniform(size=(mate.numStruts,3))

          child.C[0:self.numStruts,0:self.num_nodes] += self.C[0:self.numStruts,0:self.num_nodes]
          child.C[new_num_struts:new_num_struts+self.numStruts,0:self.num_nodes] += self.C[self.numStruts:self.numStruts+self.numStruts,0:self.num_nodes]

      else:
          child.nodes[0:new_num_struts,:] += self.nodes[0:new_num_struts,:] * p_node_self[0:new_num_struts,:]
          child.nodes[new_num_struts:new_num_struts+new_num_struts,:] += self.nodes[self.numStruts:self.numStruts+new_num_struts,:] * p_node_self[new_num_struts:new_num_struts+new_num_struts,:]

          child.C[0:new_num_struts,0:new_num_nodes] += self.C[0:new_num_struts,0:new_num_nodes]
          child.C[new_num_struts:new_num_struts+new_num_struts,0:self.num_nodes] += self.C[self.numStruts:self.numStruts+new_num_struts,0:new_num_nodes]

      # print("---------- NODES ------------")
      # print(child.nodes)
      # print(self.nodes)
      # print(mate.nodes)

      zero_base_strut =  np.minimum(self.numStruts, mate.numStruts)
      zero_base_node = np.minimum(self.num_nodes, mate.num_nodes)

      child.C[0:zero_base_strut,0:zero_base_node] /= 2
      child.C[new_num_struts:new_num_struts+zero_base_strut,0:zero_base_node] /= 2
      mask = np.random.rand(new_num_nodes,new_num_nodes)
      child.L = np.zeros((new_num_nodes,new_num_nodes))

      mask1 = child.C >= mask
      child.C[mask1] = 1
      child.L[mask1] = 1 #string connections


      #
      # for i in np.arange(new_num_struts):
      #      C_new[i,i+new_num_struts] = 0
      #      C_new[i+new_num_struts,i] = 0
      #      L[i+new_num_struts,i] = 10
      #      L[i,i+new_num_struts] = 10
      #
      # new_connections[np.eye(self.numElements*2)==1] = 0
      # L[np.eye(self.numElements*2)==1] = -1 #small number to avoid nans
      #
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
       L[np.eye(self.numElements*2)==1] = -1 #small number to avoid nans

       for i in np.arange(self.numElements):
           C[i,i+self.numElements] = 0
           C[i+self.numElements,i] = 0
           L[i+self.numElements,i] = self.length
           L[i,i+self.numElements] = self.length

       self.L = L
       self.C = C
