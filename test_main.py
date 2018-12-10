import unittest

from FormFinder import FormFinder
from Element import Element
from Structure import Structure
from Vizulization import Vizulization
from Evolution import Evolution
import numpy as np
import matplotlib.pyplot as plt
import copy
# To test:

#does the solver work for random values of theta ? past pi and -pi
class TestMain(unittest.TestCase):
    def test_save(self):
        GA1 = Evolution(num_struts = 3, strut_length = 10, max_gen=5,init_size =3, pop_size=3, mutation_rate=0.8, \
        selection_rate = 0.3, selection_pressure = 1.85,elite_rate=1)

        GA4 = Evolution(num_struts = 3, strut_length = 10, max_gen=5,init_size =3, pop_size=3, mutation_rate=0.8, \
        selection_rate = 0.3, selection_pressure = 1.85,elite_rate=1)
        GA1.current_gen = 25
        GA1.save(1)
        old_First = GA1.pop[0][2]
        old_Second = GA1.pop[1][2]

        GA4.current_gen = 50
        GA4.save(2)
        second_GA4 = GA4.pop[1][2]

        GA2 = Evolution(num_struts = 3, strut_length = 10, max_gen=5,init_size =3, pop_size=3, mutation_rate=0.8, \
        selection_rate = 0.3, selection_pressure = 1.85,elite_rate=1)
        GA2.load(25)
        new_First = GA2.pop[0][2]
        new_Second = GA2.pop[1][2]

        print(old_First.L)
        print(new_First.L)
        self.assertTrue(np.array_equal(old_First.L,new_First.L))
        self.assertTrue(np.array_equal(old_First.C,new_First.C))
        self.assertFalse(np.array_equal(old_Second.C,new_Second.C))
        self.assertFalse(np.array_equal(old_Second.C,new_Second.C))

        GA2.load(50)
        second_GA4_copy = GA2.pop[1][2]

        self.assertTrue(np.array_equal(second_GA4.L,second_GA4_copy.L))
        self.assertTrue(np.array_equal(second_GA4.C,second_GA4_copy.C))


    def test_getMateMask(self):
        droneA = Structure(10,2)
        mask = droneA.getMateMask(10,5)
        self.assertEqual(np.sum(mask[-1,:]),5)
        mask = droneA.getMateMask(10,0)
        self.assertEqual(np.sum(mask[-1,:]),0)
        mask = droneA.getMateMask(10,10)
        self.assertEqual(np.sum(mask[-1,:]),10)
    def test_reset(self):
        droneA = Structure(10,2)
        before = droneA.nodes
        droneA.resetElements()
        droneA.refresh()
        now = droneA.nodes
        self.assertTrue(np.sum(before-now) != 0)



    def test_combine_evolve(self):
        size = 2
        C = np.array([[0, 1, 0, 1],
                    [1, 0, 1, 0],
                    [0, 1, 0, 1],
                    [1, 0, 1, 0]])
        p1 = Structure(10,size,seed_C=C, seed = True)
        p2 = Structure(10,size,seed_C=C, seed = True)
        p = 0.99
        child = p1.combine(p2,ratio=p)
        p_c = 1 - p
        p_m = p
        test_L = p1.L * p_c + p2.L * p_m

        self.assertTrue(np.array_equal(test_L,child.L))
        C1 = np.array([[0, 1, 0, 1],
                    [1, 0, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]])
        C2 = np.array([[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 1, 0, 1],
                    [1, 0, 1, 0]])
        p1 = Structure(10,size,seed_C=C1, seed = True)
        p2 = Structure(10,size,seed_C=C2, seed = True)
        child = p1.combine(p2,ratio=0.4,seed=True)

        self.assertTrue(np.array_equal(child.L[:2,:],p1.L[:2,:]))
        self.assertTrue(np.array_equal(child.L[2:4,:],p2.L[2:4,:]))



    def test_length_search(self):
        Viz = Vizulization(2,2)
        Solver = FormFinder(max_iter = 1000, error_esp = 0.001, viz = Viz, show = False)

        GA = Evolution(num_struts = 3, strut_length = 10, max_gen=5,init_size =3, pop_size=3, mutation_rate=0.8, \
        selection_rate = 0.3, selection_pressure = 1.85,elite_rate=1)
        size = 3
        n = size * 2
        max_iter = 500
        C = np.array([[0, 1, 0, 1],
                    [1, 0, 1, 0],
                    [0, 1, 0, 1],
                    [1, 0, 1, 0]])
        C = np.array([[0, 1, 1, 0, 1, 0],
                      [1, 0, 1, 0, 0, 1],
                      [1, 1, 0, 1, 0, 0],
                      [0, 0, 1, 0, 1, 1],
                      [1, 0, 0, 1, 0, 1],
                      [0, 1, 0, 1, 1, 0]])
        droneA = Structure(10,size,seed_C=C, seed = True)

        droneB = droneA.duplicate()
        droneB.mutateL(step_size = 1, num_mutate = 0, p_c = 1)
        self.assertTrue(np.array_equal(droneA.L,droneB.L))

        droneB.mutateL(step_size = 1, num_mutate = 2, p_c = 1)
        self.assertEqual(np.sum(droneA.L != droneB.L),4)

        last_fit = 0
        for i in np.arange(2):

            droneB = droneA.duplicate()
            num = np.random.randint(1,np.ceil(1*droneB.numStruts)+1)
            droneB.mutateL(step_size = 1, num_mutate = num, p_c = 1)
            if 0.1 > np.random.rand():
                droneB.resetElements()
            droneB.refresh()
            Solver.solve(droneB, 1) # drones have already been solved so they go very fast
            fit = GA.fitness(droneB)

            if fit >= last_fit:
                last_fit = fit
                droneA = droneB


    def test_space_search(self):
        size = 3
        n = size * 2
        comb = (n*(n+1)/2) - (1.5*n)
        n_comb = 2**comb
        full = np.ones((size*2,size*2))
        for i in np.arange(size): #ensure valid C
            full[i,i] = 0
            full[i+size,i+size] = 0
            full[i,i+size] = 0 #don't connect to you self
            full[i+size,i] = 0
        max_iter = n_comb*2
        droneA = Structure(10,size)
        for i in np.arange(max_iter):
            droneA.mutateC()
            diff = np.sum(np.abs(droneA.C - full))
            if (np.array_equal(droneA.C,full)):
                self.assertTrue(True)
                break

            if i == max_iter - 1:
                self.assertTrue(False)

    def test_niche(self):
        GA = Evolution(num_struts = 3, strut_length = 10, max_gen=5,init_size =3, pop_size=3, mutation_rate=0.8, \
        selection_rate = 0.3, selection_pressure = 1.85,elite_rate=1)
        GA.niche_alpha = 1
        GA.niche_radius = 4
        #manually add to eval queue
        droneA = Structure(10,2)
        droneA.C = np.array([[0, 1, 0, 0],
                    [1, 0, 1, 0],
                    [0, 1, 0, 1],
                    [0, 0, 1, 0]])
        droneB = droneA.duplicate()
        droneC = Structure(10,2)
        droneC.C = np.array([[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]])
        droneD = Structure(10,2)
        droneD.C = np.array([[0, 0, 0, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 0, 0, 0]])
        GA.addToQueue(droneA, 10)
        GA.addToQueue(droneB, 10)
        GA.addToQueue(droneC, 10)
        GA.addToQueue(droneD, 10)
        GA.niche()
        self.assertEqual(GA.eval_pop[0][0],GA.eval_pop[1][0])
        self.assertEqual(GA.eval_pop[2][0],GA.eval_pop[3][0])
    def test_evolution(self):
        # plt.ion()
        Viz = Vizulization(2,2)
        Solver = FormFinder(max_iter = 100,viz=Viz,show=False)

        GA = Evolution(num_struts = 3, strut_length = 10, max_gen=2,init_size =3, pop_size=3, mutation_rate=0.8, \
        selection_rate = 0.3, selection_pressure = 1.85,elite_rate=1) #Essentailly just have an autmated hill climber rn, b/c mutation rate is so highself.

        while GA.alive():
            for i in np.arange(len(GA.pop)):
                drone_structure = GA.pop[i][2] # loop through current population
                self.assertEqual(Solver.step_move, 1)
                self.assertEqual(Solver.step_rotate, 1)
                Solver.solve(drone_structure, i) # drones have already been solved so they go very fast
                fit = GA.fitness(drone_structure) # evaluate drone
                drone_structure.fitness = fit # update fitness
                GA.addToQueue(drone_structure, fit)
            GA.elite() #p constant that first is selected.

            GA.nextGen()


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
        self.assertTrue(np.isclose(Z.L,X.L).all())

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
