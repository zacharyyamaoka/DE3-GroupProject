import numpy as np

class Element():
  def __init__(self, x=0, y=0, z=0, alpha=0, beta=0, gamma=0, length=0, k=0, random = False):
      self.k = k
      self.length = length
      self.node1 = np.array([[-length/2],[0],[0]])
      self.node2 = np.array([[length/2],[0],[0]])

      self.x_bounds = (-10,10)
      self.y_bounds = (-10,10)
      self.z_bounds = (-10,10)
      self.alpha_bounds = (-3.14,3.14)
      self.beta_bounds = (-3.14,3.14)
      self.gamma_bounds = (-3.14,3.14)

      if (random):
          x, y, z, alpha, beta, gamma = self.getRandomFrame()
      self.x = x
      self.y = y
      self.z = z
      self.alpha = alpha
      self.beta = beta
      self.gamma = gamma

      self.position = self.getFrame()

  def getRandomFrame(self):

      x = np.random.uniform(self.x_bounds[0],self.x_bounds[1],1)[0]
      y = np.random.uniform(self.y_bounds[0],self.y_bounds[1],1)[0]
      z = np.random.uniform(self.z_bounds[0],self.z_bounds[1],1)[0]
      alpha = np.random.uniform(self.alpha_bounds[0],self.alpha_bounds[1],1)[0]
      beta = np.random.uniform(self.beta_bounds[0],self.beta_bounds[1],1)[0]
      gamma = np.random.uniform(self.gamma_bounds[0],self.gamma_bounds[1],1)[0]

      return x, y, z, alpha, beta, gamma

  def wiggle( x, y, z, alpha, beta, gamma):
      self.x += x
      self.y += y
      self.z += z
      self.alpha += alpha
      self.beta += beta
      self.gamma += gamma

      self.position = self.getFrame()

  def getNodePosition(self, nodeId):
      R = self.position[0]
      P = self.position[1]

      if (nodeId == 1):
          return R.dot(self.node1) + P

      if nodeId == 2:
          return R.dot(self.node2) + P

  def getFrame(self):

      ca = np.cos(self.alpha)
      sa = np.sin(self.alpha)
      cb = np.cos(self.beta)
      sb = np.sin(self.beta)
      cy = np.cos(self.gamma)
      sy = np.sin(self.gamma)

      R = [[ca*cb, ca*sb*sy-sa*cy, ca*sb*cy+sa*sy],[sa*cb, sa*sb*sy-ca*cy, sa*sb*cy-ca*sy],[-sb, cb*sy, cb*cy]]
      R = np.array(R)#.reshape((3,3))
      P = [[self.x],[self.y],[self.z]]
      P = np.array(P)
      frame = (R, P)
      return frame
