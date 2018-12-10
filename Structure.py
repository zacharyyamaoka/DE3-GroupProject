import numpy as np
from Element import Element
import copy

class Structure():
  uniqueId = 0
  def __init__(self, length = 0, numStruts = 0, init = True, seed_C = 0, seed = False):
      # self.x_bounds = (-10,10)
      # self.y_bounds = (-10,10)
      # self.z_bounds = (-10,10)
      # self.alpha_bounds =
      # self.alpha_bounds =
      # self.alpha_bounds =
      self.mutated = False
      self.uniqueId = Structure.uniqueId
      Structure.uniqueId += 1
      self.parentId = 0
      self.numStruts = numStruts
      self.num_nodes = numStruts * 2
      self.k = 5
      if init:
          self.initStruts(numStruts, length, seed)
          self.initNodes(self.elements)
          self.initConnections(seed_C, seed)

      self.D = np.zeros((numStruts*2,numStruts*2))
      self.F = np.zeros((numStruts*2,numStruts*2))
      self.F = np.zeros((numStruts*2,numStruts*2))
      self.Delta = np.zeros((numStruts*2,numStruts*2))
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


      self.overIterated = False
      # Mutation Information
      self.wire_mutate_step = np.sqrt(self.length)
      self.strut_mutate_step = np.sqrt(self.length)
      self.connection_mutate_scale = 1
  def duplicate(self):
      new = copy.deepcopy(self)
      new.uniqueId = Structure.uniqueId
      new.parentId = self.uniqueId
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



  def getMateMask(self, total_nodes, mate_nodes):
      inds = np.random.choice(total_nodes,mate_nodes,replace=False)
      mask = np.zeros((total_nodes,total_nodes))
      for i in inds:
          mask[i,i:] = 1 #set row to 1
          mask[i:,i] = 1 #set all cols
      return mask
  def combine(self, mate, ratio=np.random.rand(), seed = False):
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

      child.C = np.zeros((new_num_nodes,new_num_nodes))
      child.L = np.zeros((new_num_nodes,new_num_nodes))
      # child.nodes = np.zeros((new_num_nodes,3))

      child.numStruts = new_num_elements
      child.num_nodes = new_num_nodes
      child.numElements = new_num_elements

      # Update Elements with cross over
      if 0.5 > np.random.rand(): #Swtich order that you combine then two -- You just take element positon from here, you do a full combine of the lengths
        new_elements = child.elements[0:element_self]
        new_elements.extend(mate.elements[element_self:element_self+element_mate])

      else: #element mate first
        new_elements = mate.elements[0:element_mate]
        new_elements.extend(self.elements[element_mate:element_self+element_mate])

      child.elements = new_elements

      # p_mate_L = np.random.rand(new_num_nodes,new_num_nodes)
      # p_mate_L = (p_mate_L + p_mate_L.T)/2
      p_mate_L = np.ones((new_num_nodes,new_num_nodes)) * p_mate
      p_mate_L[mate.L==0] = 0
      p_mate_L[self.L==0] = 1
      # go through and make some of the 0.3's to 1s min and maxing essentially.
      # p_mate_L = self.getMateMask(new_num_nodes,mate_num_nodes);
      p_self_L = -p_mate_L + 1
      new_C = p_mate*mate.C + p_self * self.C
      new_L = p_mate_L*mate.L + p_self_L * self.L

      mask = np.random.rand(new_num_nodes,new_num_nodes)
      if seed:
          mask = np.zeros((new_num_nodes,new_num_nodes)) + 0.01
      mask = (mask + mask.T)/2
      new_connection = new_C >= mask
      new_length = np.copy(new_connection)
      child.C[new_connection] = 1 #Elasticity of Connection

      new_L_connect = np.random.uniform(0,self.length,size=(self.num_nodes,self.num_nodes))
      zero = new_L == 0
      new_L[zero & new_length] = ((new_L_connect + new_L_connect.T)/2)[zero & new_length]## you need to add
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


  def initStruts(self, numStruts, length, seed = False):
      self.elements = []
      self.numElements = numStruts
      self.numStruts = numStruts
      self.length = length
      for i in np.arange(numStruts):
           if not seed:
               length=np.random.uniform(length)
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

  def getCombineLMask(self,n,L):
      new_mask = np.zeros((self.num_nodes,self.num_nodes))

      if n == 0:
          return new_mask == 1

      inds = np.random.choice(n,num_of_connections,replace=False)
      # inds = np.array([1, 2])
      start = 0
      end = self.numElements*2
      pointer = 0
      for i in np.arange(end):
          start += 1
          for j in np.arange(start,end):
              if self.C[i,j] == 1:
                  if np.any(inds == pointer):
                      new_mask[i,j] = 1
                      new_mask[j,i] = 1
                  pointer += 1
      return new_mask == 1

  def getMutateLMask(self, num_of_connections*2):

      n = int(np.sum(self.C)/2) #divide by 2 to avoid double counting
      new_mask = np.zeros((self.num_nodes,self.num_nodes))

      if n == 0:
          return new_mask == 1
      inds = np.random.choice(n,num_of_connections,replace=False)
      # inds = np.array([1, 2])
      start = 0
      end = self.numElements*2
      pointer = 0
      for i in np.arange(end):
          start += 1
          for j in np.arange(start,end):
              if self.C[i,j] == 1:
                  if np.any(inds == pointer):
                      new_mask[i,j] = 1
                      new_mask[j,i] = 1
                  pointer += 1
      return new_mask == 1

  def mutateL(self, step_size=1, num_mutate = 4, p_c = 0.5):
      #be ware the bad apple principle
      if 1-p_c < np.random.rand():
          selector = self.getMutateLMask(num_mutate)# where you have a elastic connection
          large_mutator = np.random.normal(scale = step_size * self.wire_mutate_step, size=(self.num_nodes,self.num_nodes))
          large_mutator = (large_mutator + large_mutator.T)/2 #ensure symmetry
          self.L[selector] += large_mutator[selector]
          # i = np.random.randint(self.numElements)
      else:
          for i in np.arange(self.numElements): # mutate the bar lengths by some amount aswell

              mutation = np.random.normal(scale = step_size * self.strut_mutate_step)
              curr_length = self.L[i+self.numElements,i]
              new_length = curr_length + mutation
              new_length = abs(new_length)
              new_length = np.minimum(new_length,self.length) # caps bars at maxiumum length
              self.L[i+self.numElements,i] = new_length
              self.L[i,i+self.numElements] = new_length
              self.elements[i].mutateLength(new_length)

      self.L = np.abs(self.L) #ensures no negative lengths

  def mutateC(self, step_size=1):
      noise = np.random.normal(scale = step_size * self.connection_mutate_scale, size=(self.num_nodes,self.num_nodes))
      self.C = self.C + noise
      self.C = (self.C + self.C.T)/2

      new_C = np.zeros((self.num_nodes,self.num_nodes))
      # new_L = np.zeros((self.num_nodes,self.num_nodes))
      for i in np.arange(self.numElements): #ensure valid C
          self.C[i,i] = 0
          self.C[i+self.numElements,i+self.numElements] = 0
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
      new_L = np.random.uniform(0,self.length/2,size=(self.num_nodes,self.num_nodes))
      new_L =  (new_L + new_L.T)/2
      self.L[(new_connection) & (zero)] = new_L[(new_connection) & (zero)]  # Reinitalize with random resting length

      new_C[new_connection] = 1
      self.C = new_C

  def updateElementNodes(self,ind):
      self.nodes[ind,:] = self.elements[ind].getNodePosition(1).T
      self.nodes[ind + self.numStruts,:] = self.elements[ind].getNodePosition(2).T

  def initConnections(self, seed_C = 0, seed = False):


       C = np.random.rand(self.numElements*2,self.numElements*2)
       L = np.zeros((self.numElements*2,self.numElements*2))
       #ensure symmetry
       C = C/2 + C.T/2
       if seed:
           C = seed_C
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
       # C = np.array([[0, 0, 0, 0],
       #            [0, 0, 0, 0],
       #            [0, 0, 0, 0],
       #            [0, 0, 0, 0]])

       new_connection = C>=0.5
       C[C<0.5] = 0
       new_L = np.random.uniform(0,self.length/2,size=(self.num_nodes,self.num_nodes))
       L[new_connection] =  ((new_L + new_L.T)/2)[new_connection]# intial wire length
       C[new_connection] = 1 # Spring Constant

       for i in np.arange(self.numElements):
           C[i,i] = 0
           C[i+self.numElements,i+self.numElements] = 0

           C[i,i+self.numElements] = 0
           C[i+self.numElements,i] = 0

           L[i,i] = 0
           L[i+self.numElements,i+self.numElements] = 0

           L[i+self.numElements,i] = self.elements[i].length
           L[i,i+self.numElements] = self.elements[i].length

       self.L = L
       self.C = C
