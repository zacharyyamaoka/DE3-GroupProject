import numpy as np

def Distance(node1, node2):
    return np.sqrt((node1.x - node2.x)**2 + (node1.y- node2.y)**2 + (node1.z- node2.z)**2)
