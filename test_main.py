import unittest

from FormFinder import FormFinder
from Element import Element
from Structure import Structure
from Vizulization import Vizulization
from Evolution import Evolution
import numpy as np
class TestMain(unittest.TestCase):

    def test_combine_L(self):
        X = Structure(10,8)
        D = X.duplicate()
        Y = Structure(10,3)
        Z = X.combine(Y,0.5)
        self.assertTrue(np.array_equal(D.L,X.L))
        self.assertTrue(np.array_equal(D.C,X.C))
        self.assertTrue(np.array_equal(D.nodes,X.nodes))
        for i in np.arange(Z.numStruts):
            self.assertEqual(Z.L[i+Z.numStruts,i],Z.length)
            self.assertEqual(Z.L[i,i+Z.numStruts],Z.length)
            self.assertEqual(Z.L[i,i],0)

        Z = X.combine(Y,0)
        self.assertEqual(Z.numStruts,X.numStruts)
        self.assertTrue(np.array_equal(Z.L,X.L))
        self.assertTrue(np.array_equal(Z.C,X.C))
        self.assertTrue(np.array_equal(Z.nodes,X.nodes))

        Z = X.combine(Y,1)

        self.assertEqual(Z.numStruts,Y.numStruts)
        self.assertTrue(np.array_equal(Z.L,Y.L))
        self.assertTrue(np.array_equal(Z.C,Y.C))
        self.assertTrue(np.array_equal(Z.nodes,Y.nodes))
    def test_combine_C(self):
        X = Structure(10,8)
        Y = Structure(10,3)
        Z = X.combine(Y,0.5)

        for i in np.arange(Z.numStruts):
            self.assertEqual(Z.C[i+Z.numStruts,i],0)
            self.assertEqual(Z.C[i,i+Z.numStruts],0)
            self.assertEqual(Z.C[i,i],0)

    def test_combine_nodes(self):

        X = Structure(10,8)
        Y = Structure(10,3)
        Z = X.combine(Y,0.5)

        self.assertEqual(Z.numStruts,5)
        self.assertEqual(Z.num_nodes,10)
        self.assertTrue((Z.nodes[0,:] == Y.nodes[0,:]).all())
        self.assertTrue((Z.nodes[5,:] == Y.nodes[3,:]).all())
        self.assertTrue((Z.nodes[1,:] == X.nodes[1,:]).all())
        self.assertTrue((Z.nodes[6,:] == X.nodes[9,:]).all())

    def test_combine(self):
        A = Structure(10,4)
        B = A.duplicate()

        C = A.combine(B,0.5)
        self.assertTrue((C.nodes == A.nodes).all())
        C = A.combine(B,1)
        self.assertTrue((C.nodes == A.nodes).all())
        C = A.combine(B,0)
        self.assertTrue((C.nodes == A.nodes).all())

        D = B.combine(A)
        self.assertTrue((D.nodes == B.nodes).all())

        E = A.combine(C)
        self.assertTrue((E.nodes == A.nodes).all())

        F = Structure(10,3)
        G = Structure(10,3)
        H = F.combine(G)
        self.assertEqual(H.numStruts,3)
        self.assertEqual(H.num_nodes,6)
        self.assertEqual(np.sum(H.C - H.C.T),0) #check for symetry

if __name__ == '__main__':
    unittest.main()
