# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testHabitatSimpleInput.py
# Copyright (C) 2016 flossCoder
# 
# testHabitatSimpleInput.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testHabitatSimpleInput.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testHabitatSimpleInput for testing the habitatSimpleInput.

import unittest

from habitatSimpleInput import HabitatSimpleInput
from helper import listsEqualTest, getComparator5x4
from setupTests import DIRECTORY
from testTransformer import TestTransformer
from zeroCA import zeroCA

## Test the HabitatSimpleInput class.
class TestHabitatSimpleInput(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        self.__coordinateTransformer = TestTransformer()
        self.__caInitName = "testCA"
        self.__numx = 5
        self.__numy = 4
        self.__theta = 22.0
        self.__m = 1.5
        self.__r = 2.0
        self.__qName = "testQuality"
        self.__habitatSimpleInput = HabitatSimpleInput(self.__coordinateTransformer,
                                                       self.__caInitName,
                                                       DIRECTORY,
                                                       self.__numx,
                                                       self.__numy,
                                                       self.__theta,
                                                       self.__m,
                                                       self.__r,
                                                       self.__qName)
        # set up data structure needed for comparison
        self.__ca = getComparator5x4()
        self.__quality = zeroCA(1, self.__numx, self.__numy)
        self.__quality[0][0] = 0.1
        self.__quality[0][1] = 0.2
        self.__quality[0][2] = 0.3
        self.__quality[0][3] = 0.4
        self.__quality[1][0] = 0.2
        self.__quality[1][1] = 0.3
        self.__quality[1][2] = 0.4
        self.__quality[1][3] = 0.1
        self.__quality[2][0] = 0.3
        self.__quality[2][1] = 0.4
        self.__quality[2][2] = 0.1
        self.__quality[2][3] = 0.2
        self.__quality[3][0] = 0.4
        self.__quality[3][1] = 0.1
        self.__quality[3][2] = 0.2
        self.__quality[3][3] = 0.3
        self.__quality[4][0] = 0.4
        self.__quality[4][1] = 0.3
        self.__quality[4][2] = 0.2
        self.__quality[4][3] = 0.1
    
    ## Finish the test.
    def tearDown(self):
        pass
    
    ## Test the getInitialState function.
    def testGetInitialState(self):
        equal = listsEqualTest(self.__habitatSimpleInput.getInitialState(), self.__ca)
        self.assertTrue(equal, "testGetInitialState failed")
    
    ## Test the getDataOfCell function.
    def testGetDataOfCell(self):
        for i in range(self.__numx):
            for j in range(self.__numy):
                equal = listsEqualTest(self.__habitatSimpleInput.getDataOfCell(0, [i, j]),
                               [self.__theta, self.__m, self.__r, self.__quality[i][j]])
                self.assertTrue(equal, "testGetDataOfCell failed")