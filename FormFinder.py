import numpy as np
class FormFinder():
  def __init__(self):
      pass
  def solve(self, tensegrity):
      tensegrity = 0
      info = 0
      return (tensegrity, info)

  def evalute(self, tensegrity):

      #create displacment matrix
      num_nodes = tensegrity.numStruts*2

      nodes = tensegrity.nodes.reshape(tensegrity.numElements*2,1,3)
      nodesT = tensegrity.nodes.reshape(1,num_nodes,3)
      nodesT = np.tile(nodesT,(num_nodes,1,1))
      nodes = np.tile(nodes,(1,num_nodes,1))

      D = nodesT - nodes
      info = D
      return info
