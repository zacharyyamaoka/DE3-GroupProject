import numpy as np
def similar(droneA, droneB):
    return np.sum(np.abs(droneA.C - droneB.C))
