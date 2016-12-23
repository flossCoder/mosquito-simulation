# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testStackCA.py
# Copyright (C) 2016 flossCoder
# 
# testStackCA.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testStackCA.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testStackCA for testing the stackCA.

import unittest

from helper import PseudoController, listsEqualTest, getZero
from stackCA import StackCA
from testRule import TestRule

## Test the StackCA independent of the SimulationController and the CombiCA. For this purpose the
# PseudoController is needed. The TestRule is the used rule.
class TestStackCA(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        # the controller now behaves like a CombiCA
        self.__controller = PseudoController(TestRule(False)) # no dispersion
        self.__numx = 5
        self.__numy = 5
        self.initCA = getZero(self.__numx, self.__numy)
        self.initCA[2][2] = [10, 10]
        self.__stackCA = StackCA(self.__controller, self.__numx, self.__numy, self.initCA)
    
    ## Finish the test.
    def tearDown(self):
        pass
    
    ## Tests the doStep method without dispersion.
    def testDoStepWithoutDispersion(self):
        self.__controller.rule.setDispersion(False) # set dispersion False
        self.__stackCA.doStep()
        # prepare initCA
        self.initCA[2][2] = [1010, 110]
        equal = listsEqualTest(self.__stackCA.getCA(), self.initCA)
        self.assertTrue(equal, "testDoStepWithoutDispersion failed")
        self.__stackCA.doStep()
        # prepare initCA
        self.initCA[2][2] = [2010, 210]
        equal = listsEqualTest(self.__stackCA.getCA(), self.initCA)
        self.assertTrue(equal, "testDoStepWithoutDispersion failed")
        self.__stackCA.doStep()
        # prepare initCA
        self.initCA[2][2] = [3010, 310]
        equal = listsEqualTest(self.__stackCA.getCA(), self.initCA)
        self.assertTrue(equal, "testDoStepWithoutDispersion failed")
    
    ## Tests the doStep method with dispersion.
    def testDoStepWithDispersion(self):
        self.__controller.rule.setDispersion(True) # set dispersion True
        self.__stackCA.doStep()
        # prepare initCA
        self.initCA[1][1] = [1, 1]
        self.initCA[1][2] = [1, 1]
        self.initCA[1][3] = [1, 1]
        self.initCA[2][1] = [1, 1]
        self.initCA[2][3] = [1, 1]
        self.initCA[3][1] = [1, 1]
        self.initCA[3][2] = [1, 1]
        self.initCA[3][3] = [1, 1]
        equal = listsEqualTest(self.__stackCA.getCA(), self.initCA)
        self.assertTrue(equal, "testDoStepWithDispersion failed")
        self.__stackCA.doStep()
        # prepare initCA
        self.initCA[2][2] = [18, 18]
        
        self.initCA[1][1] = [4, 4]
        self.initCA[1][2] = [6, 6]
        self.initCA[1][3] = [4, 4]
        self.initCA[2][1] = [6, 6]
        self.initCA[2][3] = [6, 6]
        self.initCA[3][1] = [4, 4]
        self.initCA[3][2] = [6, 6]
        self.initCA[3][3] = [4, 4]
        
        self.initCA[0][0] = [1, 1]
        self.initCA[0][1] = [2, 2]
        self.initCA[0][2] = [3, 3]
        self.initCA[0][3] = [2, 2]
        self.initCA[0][4] = [1, 1]
        
        self.initCA[4][0] = [1, 1]
        self.initCA[4][1] = [2, 2]
        self.initCA[4][2] = [3, 3]
        self.initCA[4][3] = [2, 2]
        self.initCA[4][4] = [1, 1]
        
        self.initCA[1][0] = [2, 2]
        self.initCA[2][0] = [3, 3]
        self.initCA[3][0] = [2, 2]
        
        self.initCA[1][4] = [2, 2]
        self.initCA[2][4] = [3, 3]
        self.initCA[3][4] = [2, 2]
        equal = listsEqualTest(self.__stackCA.getCA(), self.initCA)
        self.assertTrue(equal, "testDoStepWithDispersion failed")
        self.__stackCA.doStep()
        # prepare initCA
        self.initCA[2][2] = [26, 26]
        
        self.initCA[1][1] = [12, 12]
        self.initCA[1][2] = [14, 14]
        self.initCA[1][3] = [12, 12]
        self.initCA[2][1] = [14, 14]
        self.initCA[2][3] = [14, 14]
        self.initCA[3][1] = [12, 12]
        self.initCA[3][2] = [14, 14]
        self.initCA[3][3] = [12, 12]
        
        self.initCA[0][0] = [4, 4]
        self.initCA[0][1] = [7, 7]
        self.initCA[0][2] = [8, 8]
        self.initCA[0][3] = [7, 7]
        self.initCA[0][4] = [4, 4]
        
        self.initCA[4][0] = [4, 4]
        self.initCA[4][1] = [7, 7]
        self.initCA[4][2] = [8, 8]
        self.initCA[4][3] = [7, 7]
        self.initCA[4][4] = [4, 4]
        
        self.initCA[1][0] = [7, 7]
        self.initCA[2][0] = [8, 8]
        self.initCA[3][0] = [7, 7]
        
        self.initCA[1][4] = [7, 7]
        self.initCA[2][4] = [8, 8]
        self.initCA[3][4] = [7, 7]
        equal = listsEqualTest(self.__stackCA.getCA(), self.initCA)
        self.assertTrue(equal, "testDoStepWithDispersion failed")