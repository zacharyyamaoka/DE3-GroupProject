import numpy as np
from Structure import Structure
import heapq
from StructureFunction import *
import pickle

class Evolution():
  def __init__(self,num_struts = 2, strut_length = 10, max_gen = 100,init_size = 1, pop_size=10,mutation_rate=0.01,selection_rate=0.5,selection_pressure=1.5,elite_rate=0.1):
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
      self.num_pop = pop_size
      self.initPop(init_size, num_struts, strut_length)
      self.p_c = selection_pressure
      self.sp = selection_pressure
      self.p_elite = elite_rate
      self.niche_alpha = 1
      self.niche_radius = 4
      self.filename = 'cache/population'
      self.eps = 1
  def initPop(self,num, num_struts, strut_length):
      # self.fitness = np.zeros()
      for i in np.arange(num):
          self.pop.append((self.count, self.count, Structure(strut_length,num_struts)))
          self.count += 1
      self.count = 0
          # self.pop.append(Structure(10,3))
  def alive(self):
      return self.current_gen < self.max_gen
  def kill(self):
      self.current_gen = self.max_gen
  def save(self, num = 1):
      store = []
      for i in np.arange(num):
          curr_structure = self.pop[i][2]
          store.append([curr_structure.C, curr_structure.L])
      with open(self.filename + str(self.current_gen),'wb') as f:
          pickle.dump(store, f, pickle.HIGHEST_PROTOCOL)
      # pickle.dump(self.pop[:num], file, -1)
  def load(self, iter):
      with open(self.filename+str(iter),'rb') as f:
          store = pickle.load(f)
          for i in np.arange(len(store)):
              curr_struct = self.pop[i][2]
              loaded_struct = store[i]
              curr_struct.C = loaded_struct[0]
              curr_struct.L = loaded_struct[1]
              for i in range(curr_struct.numElements):
                   curr_struct.elements[i].mutateLength(curr_struct.L[i+curr_struct.numElements,i]) #update lengths
              curr_struct.refresh()

  def nextGen(self):
      self.pop = self.new_pop
      self.new_pop = []
      self.eval_pop = []
      self.count = 0
      self.total_fitness = 0
      self.current_gen += 1
  def getAvgFitness(self):
      return self.total_fitness/self.num_pop
  def getMaxFitness(self):
      return self.eval_pop[-1][0]

  def elite(self):
       num_elite = np.ceil(self.num_pop * self.p_elite)
       num = np.minimum(num_elite,len(self.eval_pop))
       for i in np.arange(num):
           self.new_pop.append(self.eval_pop.pop())

  def selection(self):
      pop_size = len(self.eval_pop)
      num_keep = round(self.num_pop * self.p_keep)
      if num_keep == 0:
          return
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
          accuml += fit
          threshold[i] = accuml

      threshold /= accuml

      runner = start
      counter = 0
      for i in np.arange(pop_size):
        checkpoint = threshold[i]

        while checkpoint > runner and counter < num_keep:
            self.new_pop.append(np.copy(self.eval_pop[i]))

            runner += step_size

            counter += 1


  def remove(self, p):
      num_keep = int(round((1-p)*self.num_pop))
      self.pop = heapq.nlargest(num_keep,self.eval_pop)
          # new_pop.append(item[2]) # add drone to pop
  def crossOver(self):
      curr_pop_num = len(self.new_pop)
      old_pop_num = len(self.eval_pop)
      num_cross = self.num_pop - curr_pop_num
      num_cross = np.minimum(curr_pop_num,num_cross) #for story telling
      #pick two random integers that are not the same
      for i in np.arange(num_cross):
          n1 = np.random.randint(curr_pop_num)
          while True:
            n2 = np.random.randint(curr_pop_num) #change to pick from full population
            if n2 != n1:
                break
            if curr_pop_num == 1:
                break
          p1 = self.new_pop[n1][2]
          p2 = self.new_pop[n2][2] #can have case where you mate with your self..... but hopefully note very likely I can prune these away in a later step
          child = p1.combine(p2,ratio=0.5)
          self.new_pop.append((0, child.uniqueId, child))

  def mutate(self, inplace = False, p_c = 0.1, p_reset = 0.1, p_mutateL = 0.5, p_mutateLofCB = 0.5, step_c = 1, step_l = 1):
      if inplace:
          pop_size = len(self.eval_pop)
      else:
          pop_size = len(self.new_pop)
      for i in np.arange(pop_size): #right now your going to double
          if self.p_mutation > np.random.rand(): # uniform mutation rate
            if inplace:
                offspring = self.eval_pop[i][2]
            else:
                offspring = self.new_pop[i][2].duplicate()

            if p_c > np.random.rand():
                offspring.mutateC(step_c) # so infruentely fails that you never get any good results with the L
            else:
                if p_mutateL == 0:
                    num = 0
                else: num = np.random.randint(1,np.ceil(p_mutateL*offspring.numStruts)+1) #pick number of struts to modify. Number of strings to modify can 
                offspring.mutateL(step_size = step_l, num_mutate = num, p_c = p_mutateLofCB)

            if p_reset > np.random.rand():
                offspring.resetElements()
            # if 0.1 > np.random.rand(): # uniform mutation rate
            offspring.refresh()
            if not inplace:
                self.new_pop.append((0, offspring.uniqueId, offspring))

  def addToQueue(self, drone, fitness):
      self.eval_pop.append((fitness, drone.uniqueId, drone))
      self.count += 1
  def niche(self, niche_radius = 2):
      """This Function loops through a queue and applies a penalty multipler to
      each fitness, proportional to how similar it is to the other drone_structure
      in the gene pool."""

      # m will always be >= 1 b/c you compare agianst your self
      new_eval = []
      for A in self.eval_pop:
            sharing_mul = 0
            for B in self.eval_pop:
                dist = similar(A[2],B[2])

                if dist >= niche_radius:
                    pass
                else:
                    sharing_mul += 1 - (dist/niche_radius)**self.niche_alpha
            new_eval.append((A[0]/sharing_mul, A[1], A[2]))
      self.eval_pop = new_eval


  def rankQueue(self):
        self.eval_pop.sort(key = lambda x: x[0])
  def fitness(self,drone):

      drone.fitness = drone.E_total - 0 * drone.max_force
      if drone.overIterated:
          drone.fitness = 0
      self.total_fitness += drone.fitness
      return drone.fitness
