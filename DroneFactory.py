import numpy as np

class DroneFactory():
  def __init__(self, num_struts):
      self.num_struts = num_struts
      self.num_nodes = num_struts*2

  def getX(self, mean = 0, var = 1):
      X = np.random.normal(mean, np.sqrt(var), size = (self.num_nodes, 1, 3))
      return X

  def getL(self):
      L = np.zeros((self.num_nodes,self.num_nodes))
      return L

  def getK(self):
      K = np.ones((self.num_nodes,self.num_nodes))
      return K

  def createDrone(self):
      drone = []
      drone.append(self.getX())
      drone.append(self.getL())
      drone.append(self.getK())

      return drone

  def order(self,number):
      new_order = []
      for i in range(number):
          drone = self.createDrone()
          new_order.append(drone)

      return new_order
