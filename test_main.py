import unittest

from FormFinder import FormFinder
from Element import Element
from Structure import Structure
from Vizulization import Vizulization
from Evolution import Evolution
import numpy as np


# To test:

#does the solver work for random values of theta ? past pi and -pi
class TestMain(unittest.TestCase):

    def test_solver(self):
        Solver = FormFinder()
        X = Structure(10,8)
        D, F, E, F_total, E_total, F_vec_total, delta = Solver.evalute(X)
        self.assertTrue(np.isclose(np.sum(F_vec_total,axis=0), np.zeros((1,3))).all())

    def test_mutate_L(self):
        X = Structure(10,8)
        X.mutateL()

        #ensure that length table is consitent with elements
        for i in np.arange(X.numElements): # mutate the bar lengths by some amount aswell
             self.assertEqual(X.L[i+X.numElements,i],X.L[i,i+X.numElements])
             self.assertEqual(X.L[i+X.numElements,i],X.elements[i].length)

        X = Structure(10,4)
        Y = X.duplicate()
        Y.L *= 2
        Z = Y.combine(X,0.5)
        self.assertTrue(np.array_equal(Z.L,X.L*1.5))


    def test_mutate_C(self):
        X = Structure(10,8)
        Y = X.duplicate()
        X.connection_mutate_scale = 0
        X.mutateC()
        self.assertTrue(np.array_equal(X.C,Y.C))
        self.assertTrue(np.array_equal(X.L,Y.L))


    def test_combine_L(self):
        X = Structure(10,3)
        D = X.duplicate()
        Y = Structure(10,3)
        Z = Y.combine(Y,0.5)
        self.assertTrue(np.array_equal(D.L,X.L))
        self.assertTrue(np.array_equal(D.C,X.C))
        self.assertTrue(np.array_equal(D.nodes,X.nodes))
        for i in np.arange(Z.numStruts):
            self.assertEqual(Z.L[i+Z.numStruts,i],Z.elements[i].length)
            self.assertEqual(Z.L[i,i+Z.numStruts],Z.elements[i].length)
            self.assertEqual(Z.L[i,i],0)

        Z = Y.combine(X)
        for i in np.arange(Z.numStruts):
            self.assertEqual(Z.L[i+Z.numStruts,i],Z.elements[i].length)
            self.assertEqual(Z.L[i,i+Z.numStruts],Z.elements[i].length)
            self.assertEqual(Z.L[i,i],0)

        Z = X.combine(Y,0)
        self.assertEqual(Z.numStruts,X.numStruts)

        self.assertTrue(np.array_equal(Z.L,X.L))
        self.assertTrue(np.array_equal(Z.C,X.C))
        self.assertTrue(np.array_equal(Z.nodes,X.nodes))

        Z = X.combine(D)
        self.assertTrue(np.array_equal(Z.L,X.L))

        Z = X.combine(Y,1)

        self.assertEqual(Z.numStruts,Y.numStruts)
        self.assertTrue(np.array_equal(Z.L,Y.L))
        self.assertTrue(np.array_equal(Z.C,Y.C))
        self.assertTrue(np.array_equal(Z.nodes,Y.nodes))


    def test_combine_C(self):
        X = Structure(10,3)
        Y = Structure(10,3)
        Z = X.combine(Y,0.5)

        for i in np.arange(Z.numStruts):
            self.assertEqual(Z.C[i+Z.numStruts,i],0)
            self.assertEqual(Z.C[i,i+Z.numStruts],0)
            self.assertEqual(Z.C[i,i],0)

    def test_combine_nodes(self):

        X = Structure(10,5)
        Y = Structure(10,5)
        Z = X.combine(Y,1)
        self.assertEqual(Z.numStruts,5)
        self.assertEqual(Z.num_nodes,10)
        self.assertTrue((Z.nodes[0,:] == Y.nodes[0,:]).all())
        self.assertTrue((Z.nodes[3,:] == Y.nodes[3,:]).all())
        self.assertTrue((Z.nodes[1,:] == Y.nodes[1,:]).all())
        Z = X.combine(Y,0)
        self.assertEqual(Z.numStruts,5)
        self.assertEqual(Z.num_nodes,10)
        self.assertTrue((Z.nodes[0,:] == X.nodes[0,:]).all())
        self.assertTrue((Z.nodes[3,:] == X.nodes[3,:]).all())
        self.assertTrue((Z.nodes[1,:] == X.nodes[1,:]).all())
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
