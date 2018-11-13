import numpy as np

class FormFinder():
  def __init__(self):
      pass
      self.error_esp = 0.01
      self.max_iter = 10

  def update(self, tensegrity):


          # D, F, E, F_total, E_total = self.evalute(tensegrity) # initial Specs
          #
          # max_element = np.argmax(F_total)
          # max_force = F_total[max_element]

      # move the highest force element
      tensegrity.vibrate(tensegrity.max_element, 1)
      tensegrity.refresh()
      D, F, E, F_total, E_total = self.evalute(tensegrity)

      max_element = np.argmax(F_total)
      max_force = F_total[max_element]
      tensegrity.max_element = max_element
      tensegrity.E_total = E_total
      # # see if energy went down
      # if E_total - tensegrity.E_total < 0: # delta E is negative
      #     tensegrity.max_element = max_element
      #     tensegrity.E_total = E_total
      #     # max_force = F_total[max_element]
      # else: # did not go down
      #     tensegrity.revertElemement(tensegrity.max_element)

      info = (max_force, E_total)
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
