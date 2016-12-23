# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testDBTransformer.py
# Copyright (C) 2016 flossCoder
# 
# testDBTransformer.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testDBTransformer.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testDBTransformer for testing dbTransformer.

import unittest
from dbTransformer import DBTransformer
from helper import listsEqualTest

## TestDBTransformer defines a test for the DBTransformer class.
class TestDBTransformer(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        self.__testTransformer = DBTransformer()
    
    ## Finish the test.
    def tearDown(self):
        pass
    
    ## Test the calcInnerCoordinate function.
    def testCalcInnerCoordinate(self):
        for i in range(10):
            for j in range(10):
                equal = listsEqualTest([(i - 1), (j - 1)], self.__testTransformer.calcInnerCoordinate(i, j))
                self.assertTrue(equal, "testCalcInnerCoordinate failed")
    
    ## Test the calcOuterCoordinate function.
    def testCalcOuterCoordinate(self):
        for i in range(10):
            for j in range(10):
                equal = listsEqualTest([(i + 1), (j + 1)], self.__testTransformer.calcOuterCoordinate(i, j))
                self.assertTrue(equal, "testCalcOuterCoordinate failed")