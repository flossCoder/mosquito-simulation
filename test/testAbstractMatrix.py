# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testAbstractMatrix.py
# Copyright (C) 2016 flossCoder
# 
# testAbstractMatrix.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testAbstractMatrix.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testAbstractMatrix for testing abstractMatrix.

import unittest
from abstractMatrix import AbstractMatrix
from helper import listsEqualTest, getZero

## AbstractMatrixTest defines a test for the AbstractMatrix class.
class TestAbstractMatrix(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        self.__numx = 5
        self.__numy = 5
        self.initCA = getZero(self.__numx, self.__numy)
        self.initCA[3][4] = [42, 12] # just for testing purpose
        self.__abstractMatrix = AbstractMatrix(None, self.__numx, self.__numy, self.initCA)
        self.__testCA = getZero(self.__numx, self.__numy)
    
    ## Finish the test.
    def tearDown(self):
        pass
    
    ## Test the Moore neighborhood function.
    def testMooreNeighborhood(self):
        # test if correct neighborhood for (0, 0)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([0, 0]),
                              [[0, 1], [1, 0], [1, 1]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (1, 0)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([1, 0]),
                              [[0, 0], [0, 1], [1, 1], [2, 1], [2, 0]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (2, 0)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([2, 0]),
                              [[1, 0], [1, 1], [2, 1], [3, 1], [3, 0]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (3, 0)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([3, 0]),
                              [[2, 0], [2, 1], [3, 1], [4, 1], [4, 0]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (4, 0)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([4, 0]),
                              [[3, 0], [3, 1], [4, 1]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        
        # test if correct neighborhood for (0, 1)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([0, 1]),
                              [[0, 0], [1, 0], [1, 1], [1, 2], [0, 2]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (1, 1)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([1, 1]),
                              [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [1, 2], [0, 2], [0, 1]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (2, 1)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([2, 1]),
                              [[1, 0], [2, 0], [3, 0], [3, 1], [3, 2], [2, 2], [1, 2], [1, 1]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (3, 1)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([3, 1]),
                              [[2, 0], [3, 0], [4, 0], [4, 1], [4, 2], [3, 2], [2, 2], [2, 1]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (4, 1)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([4, 1]),
                              [[4, 0], [3, 0], [3, 1], [3, 2], [4, 2]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        
        # test if correct neighborhood for (0, 2)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([0, 2]),
                              [[0, 1], [1, 1], [1, 2], [1, 3], [0, 3]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (1, 2)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([1, 2]),
                              [[0, 1], [1, 1], [2, 1], [2, 2], [2, 3], [1, 3], [0, 3], [0, 2]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (2, 2)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([2, 2]),
                              [[1, 1], [2, 1], [3, 1], [3, 2], [3, 3], [2, 3], [1, 3], [1, 2]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (3, 2)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([3, 2]),
                              [[2, 1], [3, 1], [4, 1], [4, 2], [4, 3], [3, 3], [2, 3], [2, 2]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (4, 2)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([4, 2]),
                              [[4, 1], [3, 1], [3, 2], [3, 3], [4, 3]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        
        # test if correct neighborhood for (0, 3)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([0, 3]),
                              [[0, 2], [1, 2], [1, 3], [1, 4], [0, 4]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (1, 3)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([1, 3]),
                              [[0, 2], [1, 2], [2, 2], [2, 3], [2, 4], [1, 4], [0, 4], [0, 3]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (2, 3)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([2, 3]),
                              [[1, 2], [2, 2], [3, 2], [3, 3], [3, 4], [2, 4], [1, 4], [1, 3]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (3, 3)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([3, 3]),
                              [[2, 2], [3, 2], [4, 2], [4, 3], [4, 4], [3, 4], [2, 4], [2, 3]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (4, 3)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([4, 3]),
                              [[4, 2], [3, 2], [3, 3], [3, 4], [4, 4]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        
        # test if correct neighborhood for (0, 4)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([0, 4]),
                              [[0, 3], [1, 3], [1, 4]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (1, 4)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([1, 4]),
                              [[0, 4], [0, 3], [1, 3], [2, 3], [2, 4]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (2, 4)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([2, 4]),
                              [[1, 4], [1, 3], [2, 3], [3, 3], [3, 4]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (3, 4)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([3, 4]),
                              [[2, 4], [2, 3], [3, 3], [4, 3], [4, 4]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
        # test if correct neighborhood for (4, 4)
        equal = listsEqualTest(self.__abstractMatrix._mooreNeighborhood([4, 4]),
                              [[3, 4], [3, 3], [4, 3]])
        self.assertTrue(equal, "testMooreNeighborhood failed")
    
    ## Test the getCA method. The result should be the initial CA.
    def testGetCA(self):
        equal = listsEqualTest(self.initCA, self.__abstractMatrix.getCA())
        self.assertTrue(equal, "testGetCA failed")
    
    ## Test the updateValuesOfCells function with a special test CA.
    def testUpdateValuesOfCells(self):
        testCells = [[1, 2, [5, 6]]] # cell with x = 1, y = 2, adults = 5, larvae = 6
        testCells.append([2, 3, [7, 8]]) # cell with x = 2, y = 3, adults = 7, larvae = 8
        self.__abstractMatrix._updateValuesOfCells(testCells)
        self.__testCA[1][2] = [5, 6]
        self.__testCA[2][3] = [7, 8]
        equal = listsEqualTest(self.__testCA, self.__abstractMatrix._matrixA)
        # one can't use getCA here, because the __useA has not been toggled yet
        self.assertTrue(equal, "testUpdateValuesOfCells failed")
    
    ## Test the toggleUseA function. After toggleUseA the getCA function must return the testCA.
    # Moreover matrixA must be zero.
    def testToggleUseA(self):
        self.__abstractMatrix._toggleUseA()
        # getCA should deliver the testCA
        equal = listsEqualTest(self.__testCA, self.__abstractMatrix.getCA())
        self.assertTrue(equal, "testToggleUseA failed")
        # matrixA must be zero now
        equal = listsEqualTest(self.__testCA,
                              self.__abstractMatrix._matrixA)
        self.assertTrue(equal, "testToggleUseA failed")
    
    ## Test the getOldCell function. It must return [42, 12] for cell (3, 4) after the toggleUseA
    # in the previous test.
    def testGetOldCell(self):
        equal = listsEqualTest(self.__abstractMatrix._getOldCell([3, 4]), [42, 12])
        self.assertTrue(equal, "testGetOldCell failed")