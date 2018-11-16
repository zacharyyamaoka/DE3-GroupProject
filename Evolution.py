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
  def getMaxFitness(self):
      apex = heapq.nlargest(1,self.eval_pop)
      return apex[0][0]
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
          # print(self.pop[n1][2].combine(self.pop[n2][2]))

  def mutate(self, p):
      pop_size = len(self.pop)
      fitness = pop_size
      p = 1
      for i in np.arange(pop_size): #right now your going to double
          if p > np.random.rand(): # Mutate
            curr_drone = self.pop[i][2]
            child = curr_drone.duplicate()
            child.mutateC()
            fitness += 1

            if 0.1 > np.random.rand(): # completly reset
                child.resetElements()
                child.refresh()
                self.pop.append((curr_drone.fitness-1, self.count, child))
                self.count += 1
            # # check that the child actually mutated
            elif np.sum(curr_drone.C - child.C) != 0: #check that it actually is different
                self.pop.append((fitness, self.count, child))
                self.count += 1
            else:
                print("Mutation Failed")

  def addToQueue(self, drone, fitness):
      heapq.heappush(self.eval_pop, (fitness, self.count, drone))
      self.count += 1

  def fitness(self,drone):
      # print("max force: ", drone.max_force)
      # print("total energy: ", drone.E_total)
      drone.fitness = drone.E_total - drone.max_force
      if (drone.max_force > 0.001): drone.fitness = -10000000
      return drone.fitness
