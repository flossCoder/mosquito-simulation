# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testCombiCA.py
# Copyright (C) 2016 flossCoder
# 
# testCombiCA.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testCombiCA.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testCombiCA for testing combiCA.

import unittest

from combiCA import CombiCA
from constants import EASYCA, STACKCA
from easyCA import EasyCA
from helper import getZero
from stackCA import StackCA

## TestCombiCA defines a test for the CombiCA class.
class TestCombiCA(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        self.__numx = 5
        self.__numy = 5
        self.initCA = getZero(self.__numx, self.__numy)
        self.__combiCAEasy = CombiCA(None, None, self.__numx, self.__numy, self.initCA, EASYCA)
        self.__combiCAStack = CombiCA(None, None, self.__numx, self.__numy, self.initCA, STACKCA)
    
    ## Finish the test.
    def tearDown(self):
        pass
    
    ## Test, if the setting of the CA method works correct.
    def testSetMethod(self):
        # Comment: "private" parameter / functions can be accessed from outside via
        # ob._ClassName__parameter / function.
        # Check, if everything is correct before the setMethod function is used.
        # Check parameter method.
        self.assertEqual(EASYCA,
                         self.__combiCAEasy._CombiCA__method,
                         "%s and %s are not equal" % (EASYCA, self.__combiCAEasy._CombiCA__method))
        self.assertEqual(STACKCA,
                         self.__combiCAStack._CombiCA__method,
                         "%s and %s are not equal" % (STACKCA, self.__combiCAStack._CombiCA__method))
        # Check class of parameter ca.
        self.assertEqual(type(EasyCA(None, self.__numx, self.__numy, self.initCA)),
                         type(self.__combiCAEasy._CombiCA__ca),
                         "types %s and %s are not equal" % (
                                    type(EasyCA(None, self.__numx, self.__numy, self.initCA)),
                                    type(self.__combiCAEasy._CombiCA__ca)))
        self.assertEqual(type(StackCA(None, self.__numx, self.__numy, self.initCA)),
                         type(self.__combiCAStack._CombiCA__ca),
                         "types %s and %s are not equal" % (
                                    type(StackCA(None, self.__numx, self.__numy, self.initCA)),
                                    type(self.__combiCAStack._CombiCA__ca)))
        
        # apply setCA
        self.__combiCAEasy.setCA(self.initCA, STACKCA)
        self.__combiCAStack.setCA(self.initCA, EASYCA)
        
        # do checks
        # Check parameter method.
        self.assertEqual(STACKCA,
                         self.__combiCAEasy._CombiCA__method,
                         "%s and %s are not equal" % (STACKCA, self.__combiCAEasy._CombiCA__method))
        self.assertEqual(EASYCA,
                         self.__combiCAStack._CombiCA__method,
                         "%s and %s are not equal" % (EASYCA, self.__combiCAStack._CombiCA__method))
        # Check class of parameter ca.
        self.assertEqual(type(StackCA(None, self.__numx, self.__numy, self.initCA)),
                         type(self.__combiCAEasy._CombiCA__ca),
                         "types %s and %s are not equal" % (
                                    type(StackCA(None, self.__numx, self.__numy, self.initCA)),
                                    type(self.__combiCAEasy._CombiCA__ca)))
        self.assertEqual(type(EasyCA(None, self.__numx, self.__numy, self.initCA)),
                         type(self.__combiCAStack._CombiCA__ca),
                         "types %s and %s are not equal" % (
                                    type(EasyCA(None, self.__numx, self.__numy, self.initCA)),
                                    type(self.__combiCAStack._CombiCA__ca)))
    
    ## Test, if the calcFillingDegree function works correct.
    def testCalcFillingDegree(self):
        numCells = self.__numx * self.__numy
        filled = 0 # current number of filled cells 
        # test empty CA
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        
        # fill in each run a new cell
        filled += 1
        self.initCA[0][0][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[0][1][1] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[0][2][0] = self.initCA[0][2][1] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[0][3][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[0][4][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        
        filled += 1
        self.initCA[1][0][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[1][1][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[1][2][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[1][3][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[1][4][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        
        filled += 1
        self.initCA[2][0][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[2][1][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[2][2][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[2][3][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[2][4][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        
        filled += 1
        self.initCA[3][0][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[3][1][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[3][2][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[3][3][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[3][4][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        
        filled += 1
        self.initCA[4][0][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[4][1][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[4][2][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[4][3][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))
        filled += 1
        self.initCA[4][4][0] = 42
        self.assertEqual(filled / numCells,
                         self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA),
                         "%i and %i are not equal" % ((filled / numCells),
                                self.__combiCAEasy._CombiCA__calcFillingDegree(self.initCA)))