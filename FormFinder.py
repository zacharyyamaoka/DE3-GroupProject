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
      nodesT = tensegrity.nodes.reshape(1,tensegrity.numElements*2,3)
      print(nodes.shape)
      print(nodesT.shape)
      D_full = np.tile(nodes,(1,num_nodes,1))
      D_full_T = np.tile(nodesT,(num_nodes,1,1))

      D_full = np.tile(tensegrity.nodes,(num_nodes,1))

      D_full = np.tile(tensegrity.nodes,(num_nodes,1))
      D_full = D_full.reshape((num_nodes,num_nodes,3))
      print(D_full)
      D = D_full.transpose((1,0,2)) #- D_full
      print(D)
      print(D.shape)
      info = D
      return info
