# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testEasyCA.py
# Copyright (C) 2016 flossCoder
# 
# testEasyCA.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testEasyCA.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testEasyCA for testing easyCA.

import unittest
from easyCA import EasyCA
from helper import PseudoController, listsEqualTest, getZero
from testRule import TestRule

## Test the EasyCA independent of the SimulationController and the CombiCA. For this purpose the
# PseudoController is needed. The TestRule is the used rule.
class TestEasyCA(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        # the controller now behaves like a CombiCA
        self.__controller = PseudoController(TestRule(False)) # no dispersion
        self.__numx = 5
        self.__numy = 5
        self.initCA = getZero(self.__numx, self.__numy)
        self.__easyCA = EasyCA(self.__controller, self.__numx, self.__numy, self.initCA)
        # prepare a data structure needed for the later tests
        # deltaDispersion saves the state change of a simulation with dispersion:
        # deltaDispersion = state(t) - state(t-1) 
        self.__deltaDispersion = getZero(self.__numx, self.__numy)
        # change the boundaries
        # corners
        self.__deltaDispersion[0][0] = [3, 3]
        self.__deltaDispersion[0][4] = [3, 3]
        self.__deltaDispersion[4][0] = [3, 3]
        self.__deltaDispersion[4][4] = [3, 3]
        # sides
        self.__deltaDispersion[0][1] = [5, 5]
        self.__deltaDispersion[0][2] = [5, 5]
        self.__deltaDispersion[0][3] = [5, 5]
        
        self.__deltaDispersion[4][1] = [5, 5]
        self.__deltaDispersion[4][2] = [5, 5]
        self.__deltaDispersion[4][3] = [5, 5]
        
        self.__deltaDispersion[1][0] = [5, 5]
        self.__deltaDispersion[2][0] = [5, 5]
        self.__deltaDispersion[3][0] = [5, 5]
        
        self.__deltaDispersion[1][4] = [5, 5]
        self.__deltaDispersion[2][4] = [5, 5]
        self.__deltaDispersion[3][4] = [5, 5]
        # inner
        self.__deltaDispersion[1][1] = [8, 8]
        self.__deltaDispersion[2][1] = [8, 8]
        self.__deltaDispersion[3][1] = [8, 8]
        
        self.__deltaDispersion[1][2] = [8, 8]
        self.__deltaDispersion[2][2] = [8, 8]
        self.__deltaDispersion[3][2] = [8, 8]
        
        self.__deltaDispersion[1][3] = [8, 8]
        self.__deltaDispersion[2][3] = [8, 8]
        self.__deltaDispersion[3][3] = [8, 8]
    
    ## Finish the test.
    def tearDown(self):
        pass
    
    ## Tests the doStep method without dispersion.
    def testDoStepWithoutDispersion(self):
        self.__controller.rule.setDispersion(False) # set dispersion False
        self.__easyCA.doStep()
        equal = listsEqualTest(self.__easyCA.getCA(),
                       [[[1000, 100] for i in range(self.__numx)] for j in range(self.__numy)])
        self.assertTrue(equal, "testDoStepWithoutDispersion failed")
        self.__easyCA.doStep()
        equal = listsEqualTest(self.__easyCA.getCA(),
                       [[[2000, 200] for i in range(self.__numx)] for j in range(self.__numy)])
        self.assertTrue(equal, "testDoStepWithoutDispersion failed")
        self.__easyCA.doStep()
        equal = listsEqualTest(self.__easyCA.getCA(),
                       [[[3000, 300] for i in range(self.__numx)] for j in range(self.__numy)])
        self.assertTrue(equal, "testDoStepWithoutDispersion failed")
    
    ## Tests the doStep method with dispersion.
    def testDoStepWithDispersion(self):
        self.__controller.rule.setDispersion(True) # set dispersion True
        self.__easyCA.doStep()
        self.__calcAfterDispersionStep()
        equal = listsEqualTest(self.__easyCA.getCA(), self.initCA)
        self.assertTrue(equal, "testDoStepWithDispersion failed")
        self.__easyCA.doStep()
        self.__calcAfterDispersionStep()
        equal = listsEqualTest(self.__easyCA.getCA(), self.initCA)
        self.assertTrue(equal, "testDoStepWithDispersion failed")
        self.__easyCA.doStep()
        self.__calcAfterDispersionStep()
        equal = listsEqualTest(self.__easyCA.getCA(), self.initCA)
        self.assertTrue(equal, "testDoStepWithDispersion failed")
    
    ## Helping function to calculate the state after a simulation step with dispersion to compare
    # with the result of the EasyCA (and TestRule).
    def __calcAfterDispersionStep(self):
        for i in range(self.__numx):
            for j in range(self.__numy):
                self.initCA[i][j][0] += self.__deltaDispersion[i][j][0]
                self.initCA[i][j][1] += self.__deltaDispersion[i][j][1]