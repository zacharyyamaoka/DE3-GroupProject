import numpy as np

class FormFinder():
  def __init__(self):
      pass
      self.error_esp = 0.01
      self.max_iter = 10

  def solve(self, tensegrity):
      iter = 0
      energy = []
      force = []
      D, F, E, F_total, E_total = self.evalute(tensegrity) # initial Specs

      max_element = np.argmax(F_total)
      max_force = F_total[max_element]


      while (max_force > self.error_esp) and (iter < self.max_iter):
          iter += 1
          energy.append(E_total)
          force.append(max_force)

          # move the highest force element
          tensegrity.vibrate(max_element)
          D, F, E, F_total, E_total = self.evalute(tensegrity)

          # see if energy went down
          print(iter)
          if E_total - energy[-1] < 0: # delta E is negative
              max_element = np.argmax(F_total)
              max_force = F_total[max_element]
          else: # did not go down
              tensegrity.revertElemement(max_element)

      # return (tensegrity, info)


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

      K = tensegrity.C.reshape(num_nodes,num_nodes,1)

      #begin to do this for only certain rows.
      F = D*K
      E = 0.5 * tensegrity.C * np.sum((D*D),axis=2)
      E_total = np.sum(E)
      E_total /= 2 # avoid double counting for elastics

      #Determine force on each node
      F_nodes = np.sum(F,axis=1)

      #Determine net forces on each element
      #SPLITING HELPS :) I think there
      F_total = F_nodes[:num_struts,:] + F_nodes[num_struts:,:]
      F_total = np.sum(F_total*F_total,axis=1)

      info = (D, F, E, F_total, E_total)
      return info
