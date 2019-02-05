import numpy as np
import unittest
from ga_funcs import *

# State vector
class TestMain(unittest.TestCase):

    def test_mat2gene(self):

        mat = np.random.random((4,4))
        gene = mat2gene(mat)
        size = matGeneSize(mat.shape[0])

        self.assertEqual(len(gene),size)

    def test_gene2mat(self):

        gene = np.random.random((1,4))
        gene = gene.tolist()
        print(type(gene))
        self.assertEqual(type(gene),list)
        # mat = np.random.random((4,4))
        # gene = mat2gene(mat)
        # size = matGeneSize(mat.shape[0])
        #
        # self.assertEqual(len(gene),size)

if __name__ == '__main__':
    unittest.main()
