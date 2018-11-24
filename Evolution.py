import numpy as np
from Structure import Structure
import heapq

class Evolution():
  def __init__(self,max_gen = 100,pop_size=10,mutation_rate=0.01,selection_rate=0.5,selection_pressure=1.5):
      pass
      self.max_gen = max_gen
      self.pop = []
      self.current_gen = 0
      self.new_pop = []
      self.eval_pop = []
      self.count = 0
      self.total_fitness = 0
      self.p_mutation = mutation_rate
      self.p_keep = selection_rate
      self.initPop(pop_size)
      self.p_c = selection_pressure
      self.sp = selection_pressure
  def initPop(self,num):
      self.num_pop = num
      # self.fitness = np.zeros()
      for i in np.arange(num):
          self.pop.append((self.count, self.count, Structure(10,3)))
          self.count += 1
      self.count = 0
          # self.pop.append(Structure(10,3))
  def alive(self):
      return self.current_gen < self.max_gen
  def kill(self):
      self.current_gen = self.max_gen

  def nextGen(self):
      self.pop = self.new_pop
      self.new_pop = []
      self.eval_pop = []
      self.count = 0
      self.total_fitness = 0
      self.current_gen += 1
  def getAvgFitness(self):
      return self.total_fitness/len(self.pop)
  def getMaxFitness(self):
      return self.pop[0][0]

  def selection(self):
      pop_size = len(self.eval_pop)
      num_keep = round(self.num_pop * self.p_keep)
      step_size = 1/num_keep
      start = np.random.uniform(0,step_size)
      threshold = np.zeros(pop_size)

      #intial thresholds
      accuml = 0
      for i in np.arange(pop_size):
          fit = 2 - self.sp + (2 * (self.sp-1)*(i/pop_size))
          # p = ((1-self.p_c)**i)*self.p_c
          # if (i == pop_size - 1): #last ones
          #   p = (1-self.p_c)**i
          print("P: ", fit)
          accuml += fit
          threshold[i] = accuml

      threshold /= accuml

      runner = start
      counter = 0
      print(threshold)
      for i in np.arange(pop_size):
        checkpoint = threshold[i]

        while checkpoint > runner and counter < num_keep:
            self.new_pop.append(self.eval_pop[i])

            runner += step_size

            counter += 1


  def remove(self, p):
      num_keep = int(round((1-p)*self.num_pop))
      self.pop = heapq.nlargest(num_keep,self.eval_pop)
          # new_pop.append(item[2]) # add drone to pop
  def crossOver(self):
      curr_pop_num = len(self.new_pop)
      num_cross = self.num_pop - curr_pop_num
      #pick two random integers that are not the same
      for i in np.arange(num_cross):
          n1 = np.random.randint(curr_pop_num)
          while True:
              n2 = np.random.randint(curr_pop_num)

              if n2 != n1:
                  break
              if curr_pop_num == 1:
                  break
          print("n1: ", n1)
          print("n2: ", n2)
          p1 = self.new_pop[n1][2]
          p2 = self.new_pop[n2][2]
          child = p1.combine(p2)
          self.new_pop.append((0, child.uniqueId, child))

  def mutate(self):
      pop_size = len(self.new_pop)

      for i in np.arange(pop_size): #right now your going to double
          if self.p_mutation > np.random.rand(): # uniform mutation rate
            self.new_pop[i][2].mutateC()
            self.new_pop[i][2].mutateL()
            # if 0.1 > np.random.rand(): # uniform mutation rate
            self.new_pop[i][2].resetElements()

            self.new_pop[i][2].refresh()


  def addToQueue(self, drone, fitness):
      self.eval_pop.append((fitness, drone.uniqueId, drone))
      self.count += 1
  def rankQueue(self):
        self.eval_pop.sort(key = lambda x: x[0])
  def fitness(self,drone):
      # print("max force: ", drone.max_force)
      # print("total energy: ", drone.E_total)
      drone.fitness = drone.E_total - drone.max_force
      if (drone.max_force > 0.001): drone.fitness = -10000000
      return drone.fitness
