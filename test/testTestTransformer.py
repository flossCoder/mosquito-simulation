# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testTestTransformer.py
# Copyright (C) 2016 flossCoder
# 
# testTestTransformer.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testTestTransformer.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testTestTransformer test the testTransformer package.

import unittest

from helper import listsEqualTest
from testTransformer import TestTransformer

## TestTestTransformer defines a test for the TestTransformer class.
class TestTestTransformer(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        self.__testTransformer = TestTransformer()
    
    ## Finish the test.
    def tearDown(self):
        pass
    
    ## Test the calcInnerCoordinate function.
    def testCalcInnerCoordinate(self):
        for i in range(10):
            for j in range(10):
                equal = listsEqualTest([i, j], self.__testTransformer.calcInnerCoordinate(i, j))
                self.assertTrue(equal, "testCalcInnerCoordinate failed")
    
    ## Test the calcOuterCoordinate function.
    def testCalcOuterCoordinate(self):
        for i in range(10):
            for j in range(10):
                equal = listsEqualTest([i, j], self.__testTransformer.calcOuterCoordinate(i, j))
                self.assertTrue(equal, "testCalcOuterCoordinate failed")