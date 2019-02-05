
import numpy as np

def encode(K, L, X=0):

    gene = [0]
    return gene

def decode(gene):

    K = [0]
    L = 1
    X = 1
    return K, L, X

def mat2gene(mat):
    #mat must be numpy array
    gene = []

    mat = np.array(mat)
    n =  mat.shape[0]
    for i in range(n):
        for j in range(i+1,n):
            gene.append(mat[i,j])

    return gene


def matGeneSize(n):
    return n*(n-1)/2

def gene2mat(G):
    #number of entries in top right, no diagonal = N(N-1)/2
    mat = [0]
    return mat
