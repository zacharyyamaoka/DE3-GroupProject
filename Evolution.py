import numpy as np
from Structure import Structure
import heapq

class Evolution():
  def __init__(self,max_gen = 100):
      pass
      self.max_gen = max_gen
      self.pop = []
      self.current_gen = 0
      self.new_pop = []
      self.eval_pop = []
      self.count = 0
  def initPop(self,num):
      self.num_pop = num
      # self.fitness = np.zeros()
      for i in np.arange(num):
          heapq.heappush(self.pop, (self.count, self.count, Structure(10,3)))
          self.count += 1
      self.count = 0
          # self.pop.append(Structure(10,3))
  def alive(self):
      return self.current_gen < self.max_gen
  def nextGen(self):
      self.new_pop = []
      self.eval_pop = []
      self.count = 0
      self.current_gen += 1
  def remove(self, p):
      num_keep = int(round((1-p)*self.num_pop))
      self.pop = heapq.nlargest(num_keep,self.eval_pop)
          # new_pop.append(item[2]) # add drone to pop
  def crossOver(self, p):
      num_cross = int(round(p*self.num_pop))

      #pick two random integers that are not the same
      for i in np.arange(num_cross):
          n1 = np.random.randint(0,len(self.pop))
          while True:
              n2 = np.random.randint(0,len(self.pop))
              if n2 != n1:
                  break
              if len(self.pop) == 1:
                  break
          print(self.pop[n1][2].combine(self.pop[n2][2]))

  def mutate(self, p):
      pass
  def addToQueue(self, drone, fitness):
      heapq.heappush(self.eval_pop, (fitness, self.count, drone))
      self.count += 1

  def fitness(self,drone):

      return drone.max_force
