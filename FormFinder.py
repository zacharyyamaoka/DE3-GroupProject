import numpy as np
import matplotlib.pyplot as plt

class FormFinder():
  def __init__(self, max_iter = 1000, error_esp = 0.001, viz = None, show = False):
      self.error_esp = error_esp
      self.max_iter = max_iter
      self.reject_move = 0
      self.overflow_move = 10
      self.reject_rotate = 0
      self.overflow_rotate = 10
      self.step_move = 1
      self.step_rotate = 1
      self.viz = viz
      self.show = show
      self.rejected_rotate = False
      self.rejected_move = False

      if self.show:
          self.EnergyGraph = self.viz.createGraph()
          self.viz.labelGraph(self.EnergyGraph,"EnergyGraph")
          self.ForceGraph = self.viz.createGraph()
          self.viz.labelGraph(self.EnergyGraph,"ForceGraph")
      # self.min_step = 0.001
  def reset(self):
      self.reject_move = 0
      self.overflow_move = 30
      self.reject_rotate = 0
      self.overflow_rotate = 30
      self.step_rotate = 1
      self.step_move = 1

  def solve(self, drone, ind=0):
      force = []
      energy = []

      iter = 0
      D, F, E, F_total, E_total, F_vec_total, Delta = self.evalute(drone)
      drone.max_element = np.argmax(F_total)
      drone.max_force = np.amax(F_total)
      drone.E_total = E_total
      drone.F_total = F_total
      drone.Delta = Delta
      max_force = drone.max_force
      while (max_force > self.error_esp) and (iter < self.max_iter):
          iter += 1
          max_force, E_total, sample_E = self.update(drone, 'move')
          max_force, E_total, sample_E = self.update(drone, 'rotate')
          if self.show:
              energy.append(E_total)
              force.append(max_force)

              if iter%2==0:

                  c = 'black'
                  if self.rejected_rotate:
                      self.rejected_rotate = False
                      c = 'red'
                  if self.rejected_move:
                      self.rejected_move = False
                      c = 'green'
                  self.viz.plotGraph(self.EnergyGraph,E_total,iter,c=c)
                  self.viz.plotGraph(self.ForceGraph,max_force,iter,c=c)
              if iter%10==0:
                  print("Energy: ", E_total)
                  print("Max Force: ", max_force)
                  print("ITER: ", iter)
                  self.viz.show(drone, ind)
                  plt.show()
                  plt.pause(0.1)

      if self.show:
          self.viz.clearGraph(self.EnergyGraph)
          self.viz.clearGraph(self.ForceGraph)
      drone.solved = True
      if (iter >= self.max_iter):
          drone.overIterated = True
          print("Over Iteration")
      else:
          drone.overIterated = False
      self.reset() #reset internal parameters for next time

  def update(self, tensegrity, type=''):

    #NOTE TO SELF you will have to change the max iter and step Siz
      # as the complexity of the sturcture changes

        # D, F, E, F_total, E_total = self.evalute(tensegrity) # initial Specs
        #
        # max_element = np.argmax(F_total)
        # max_force = F_total[max_element]

    # move the highest force element
    ind = np.argmax(np.random.rand(tensegrity.numStruts)*tensegrity.F_total)
    element_F = tensegrity.F_total[ind]

    if type == 'rotate':

        if (self.reject_rotate > self.overflow_rotate):
            self.step_rotate *= 0.5
            self.reject_rotate = 0
            self.rejected_rotate = True

        tensegrity.vibrate(ind, type='rotate', multipler=self.step_rotate)
        tensegrity.updateElementNodes(ind)

    if type == 'move':

        if (self.reject_move > self.overflow_move):
            self.step_move *= 0.5
            self.reject_move = 0
            self.rejected_move = True


        tensegrity.vibrate(ind, type='move', multipler=self.step_move)
        tensegrity.updateElementNodes(ind)


    D, F, E, F_total, E_total, F_vec_total, Delta = self.evalute(tensegrity)

    # see if energy went down

    if  E_total - tensegrity.E_total  < 0: # delta E is negative
        if type == 'rotate':
            self.reject_rotate = 0
        if type == 'move':
            self.reject_move = 0
        tensegrity.max_element = np.argmax(F_total)
        tensegrity.max_force = F_total[tensegrity.max_element]
        tensegrity.E_total = E_total
        tensegrity.F_total = F_total
        tensegrity.Delta = Delta
        # max_force = F_total[max_element]
    else: # did not go down
        if type == 'rotate':
            self.reject_rotate += 1
        if type == 'move':
            self.reject_move += 1

        tensegrity.revertElemement(ind)
        tensegrity.updateElementNodes(ind)

    info = (tensegrity.max_force, tensegrity.E_total, E_total)
    return info

  def evalute(self, tensegrity):

      #create displacment matrix
      num_struts = tensegrity.numStruts
      num_nodes = tensegrity.numStruts*2

      nodes = tensegrity.nodes.reshape(tensegrity.numElements*2,1,3)

      nodesT = tensegrity.nodes.reshape(1,num_nodes,3)
      nodesT = np.tile(nodesT,(num_nodes,1,1))
      nodes = np.tile(nodes,(1,num_nodes,1))

      D = nodesT - nodes # Calculate Displacement Matrix
      info = D

      # Determine forces on each node

      K = tensegrity.C * tensegrity.k #spring constant assume all strings are of the same material, but you change the intial length which seems fair.

      L_curr = np.sqrt(np.sum((D*D),axis=2))
      L_curr[np.diag_indices(num_nodes)] = -1 # to avoid nans displacement to your self
      Delta = L_curr - tensegrity.L


      Delta[Delta<0] = 0 #strings are not taught
      F = Delta*K
      F = F.reshape(num_nodes,num_nodes,1)

      F = (D/L_curr.reshape(num_nodes,num_nodes,1)) * F
      #begin to do this for only certain rows.
      # tensegrity.F = F

      E = 0.5 * tensegrity.C * Delta ** 2
      E_total = np.sum(E)
      E_total /= 2 # avoid double counting for elastics

      #Determine force on each node
      F_nodes = np.sum(F,axis=1)

      # F_node_abs = np.sum(np.abs(F),axis=1)
      #Determine net forces on each element
      #SPLITING HELPS :) I think there
      F_vec_total = F_nodes[:num_struts,:] + F_nodes[num_struts:,:]
      F_total = np.sum(F_vec_total*F_vec_total,axis=1)
      # F_vec_total[1,:] *= 1.1
      info = (D, F, E, F_total, E_total, F_vec_total, Delta)
      return info
