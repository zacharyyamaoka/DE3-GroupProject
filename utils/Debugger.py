import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Debugger():
  def __init__(self):
      plt.ion()
      self.fig = plt.figure(1)
      self.ax = self.fig.add_subplot(111,projection='3d',proj_type = 'ortho')
      # self.ax = self.fig.add_subplot(111,projection='3d')
      self.ax.set_aspect('equal')
  #Display 3D position data
  def draw_Pos(self, pos):
      #(pos has shape (timesteps,3))
      ax = self.ax
      self.pos_data = pos

      timesteps = pos.shape[0]
      for i in range(timesteps):
        ax.scatter3D(pos[i,0], pos[i,1], pos[i,2], c="b");

  def draw_X(self, X):
      ax = self.ax
      for node in X:
        ax.scatter3D(node[:,0], node[:,1], node[:,2], c="b");
  def clear(self):
      self.ax.cla()

  def drop_port(self):

      #Find mean drop data...
      X = self.pos_data[:,0]
      Y = self.pos_data[:,1]
      Z = self.pos_data[:,2]

      n = X.shape[0]
      first_third = int(n/3)

      x_mean = X[0] #np.mean(X[:,:first_third])
      x_var = 10 #np.var(X)
      y_mean = Y[0] #np.mean(Y[:,:first_third])
      y_var = 10 #np.var(Y)
      x=[x_mean-x_var,x_mean+x_var]
      y=[y_mean-y_var,y_mean+y_var]
      print(np.max(Z))
      z=[0,np.max(Z)]
      print(x, y, z)
      print(self.pos_data)
      self.fix_ratio(x, y, z, scale = 1)

  def fix_ratio(self, x=[-1.0,1.0], y=[-1.0,1.0], z=[-1.0,1.0], scale = 0.1):
      ax = self.ax

      x = np.array(x)
      y = np.array(y)
      z = np.array(z)

      x *= scale
      y *= scale
      z *= scale

      X = np.arange(x[0],x[1])
      Y = np.arange(y[0],y[1])
      Z = np.arange(z[0],z[1])

      max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
      Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
      Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
      Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
      for xb, yb, zb in zip(Xb, Yb, Zb):
          ax.plot([xb], [yb], [zb], 'w')
      ax.set_xlim([x[0],x[1]])
      ax.set_ylim([y[0],y[1]])
      ax.set_zlim([z[0],z[1]])
  def draw_K_strut(self, K, L, X, strut_K = 50):
      ax = self.ax
      print(X[[0,0],[0,0]])
      n = K.shape[0]
      for i in np.arange(n):
          row = K[i]
          for j in np.arange(n):
              if row[j] > 0:
                  rows = np.array([i,j])
                  cols = np.array([0,0])
                  colour = 'blue'
                  if row[j] == strut_K: #struts different colours
                      colour = 'red'
                  ax.plot3D(X[rows,cols,np.array([0,0])], X[rows,cols,np.array([1,1])], X[rows,cols,np.array([2,2])],c=colour)

  def draw_C(self, D, K, L, X):
      ax = self.ax
      n = D.shape[0]
      delta = D - L
      for i in np.arange(n):
          row = K[i]
          for j in np.arange(n):
              if row[j] > 0:
                  rows = np.array([i,j])
                  cols = np.array([0,0])
                  if delta[i,j] > 0: #pulling togther
                      colour = 'blue'
                  else:
                      colour = 'red' #pushing apart
                  ax.plot3D(X[rows,cols,np.array([0,0])], X[rows,cols,np.array([1,1])], X[rows,cols,np.array([2,2])],c=colour)

  def draw_D(self, D, X):
      z_offset = 0
      ax = self.ax
      num = D.shape[0]
      for i in np.arange(num):
          z_offset += 0.1
          row = D[i]
          start = X[i,0,:]
          for j in np.arange(num):
              if j != i:
                  end = row[j]
                  ax.quiver(start[0], start[1], start[2]-z_offset, end[0], end[1], end[2], normalize = False)
                  # ax.quiver(start[0], start[1], start[2], end[0], end[1], end[2], normalize = True)


  def display(self,  time=1, azimuth=0, altitude=90, drop_port = False):
      # self.ax.view_init(15,45)
      self.ax.view_init(altitude,azimuth)
      if not drop_port:
          self.fix_ratio()
      else:
          self.drop_port()
      plt.show()
      plt.pause(time)
      # plt.close()
