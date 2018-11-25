import numpy as np
x = np.arange(20)
print(x[:10])
print(x[10:20])

x = np.random.normal(loc=10,size=(3,3),scale=np.sqrt(10/3))
print(x)
print(np.minimum(x,10))
