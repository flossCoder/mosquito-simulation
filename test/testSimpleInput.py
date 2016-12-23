# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testSimpleInput.py
# Copyright (C) 2016 flossCoder
# 
# testSimpleInput.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testSimpleInput.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testSimpleInput for testing the simpleInput.

import unittest

from helper import listsEqualTest, getComparator5x4
from setupTests import DIRECTORY
from simpleInput import SimpleInput
from testTransformer import TestTransformer

## Test the SimpleInput class.
class TestSimpleInput(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        self.__coordinateTransformer = TestTransformer()
        self.__caInitName = "testCA"
        self.__numx = 5
        self.__numy = 4
        self.__theta = 22.0
        self.__m = 1.5
        self.__r = 2.0
        self.__q = 1.0
        self.__simpleInput = SimpleInput(self.__coordinateTransformer,
                                         self.__caInitName,
                                         DIRECTORY,
                                         self.__numx,
                                         self.__numy,
                                         self.__theta,
                                         self.__m,
                                         self.__r,
                                         self.__q)
        # set up data structure needed for comparison
        self.__ca = getComparator5x4()
    
    ## Finish the test.
    def tearDown(self):
        pass
    
    ## Test the getInitialState function.
    def testGetInitialState(self):
        equal = listsEqualTest(self.__simpleInput.getInitialState(), self.__ca)
        self.assertTrue(equal, "testGetInitialState failed")
    
    ## Test the getDataOfCell function.
    def testGetDataOfCell(self):
        for i in range(self.__numx):
            for j in range(self.__numy):
                equal = listsEqualTest(self.__simpleInput.getDataOfCell(0, [i, j]),
                               [self.__theta, self.__m, self.__r, self.__q])
                self.assertTrue(equal, "testGetDataOfCell failed")