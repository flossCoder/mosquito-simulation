# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testTestRule.py
# Copyright (C) 2016 flossCoder
# 
# testTestRule.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testTestRule.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testTestRule for testing the testRule package.

import unittest

from helper import resultsEqualTest
from testRule import TestRule

## Test the TestRule class.
class TestTestRule(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        self.__testRule = TestRule(False) # no dispersion
        self.__state = [0, 0] # [adults, larvae]
        self.__values = [22, 1.5, 2.0, 1.0] # [theta, m, r, q]
        self.__cell1 = [2, 2, self.__state, self.__values]
        self.__neighborhood1 = [[1, 1, self.__state, self.__values],
                                [2, 1, self.__state, self.__values],
                                [3, 1, self.__state, self.__values],
                                [1, 2, self.__state, self.__values],
                                [3, 2, self.__state, self.__values],
                                [1, 3, self.__state, self.__values],
                                [2, 3, self.__state, self.__values],
                                [3, 3, self.__state, self.__values]]
        self.__cell2 = [0, 0, self.__state, self.__values]
        self.__neighborhood2 = [[0, 1, self.__state, self.__values],
                                [1, 1, self.__state, self.__values],
                                [1, 0, self.__state, self.__values]]
        self.__cell3 = [2, 4, self.__state, self.__values]
        self.__neighborhood3 = [[1, 4, self.__state, self.__values],
                                [1, 3, self.__state, self.__values],
                                [2, 3, self.__state, self.__values],
                                [3, 3, self.__state, self.__values],
                                [3, 4, self.__state, self.__values]]
    
    ## Finish the test.
    def tearDown(self):
        pass
    
    ## Test the calculateValues function with dispersion = False.
    def testCalculateValuesWithoutDispersion(self):
        # set dispersion = False
        self.__testRule.setDispersion(False)
        equal = resultsEqualTest(self.__testRule.calculateValues(self.__cell1, self.__neighborhood1),
                               [[2, 2, [1000, 100]]])
        self.assertTrue(equal, "testCalculateValuesWithoutDispersion failed")
        equal = resultsEqualTest(self.__testRule.calculateValues(self.__cell2, self.__neighborhood1),
                               [[0, 0, [1000, 100]]])
        self.assertTrue(equal, "testCalculateValuesWithoutDispersion failed")
        equal = resultsEqualTest(self.__testRule.calculateValues(self.__cell3, self.__neighborhood1),
                               [[2, 4, [1000, 100]]])
        self.assertTrue(equal, "testCalculateValuesWithoutDispersion failed")
    
    ## Test the setDispersion function.
    def testSetDispersion(self):
        # set dispersion = True
        self.__testRule.setDispersion(True)
        self.assertTrue(self.__testRule._TestRule__dispersion, "testSetDispersion failed")
        # set dispersion = False
        self.__testRule.setDispersion(False)
        self.assertFalse(self.__testRule._TestRule__dispersion, "testSetDispersion failed")
    
    ## Test the calculateValues function with dispersion = True.
    def testCalculateValuesWithDispersion(self):
        # set dispersion = True
        self.__testRule.setDispersion(True)
        equal = resultsEqualTest(self.__testRule.calculateValues(self.__cell1, self.__neighborhood1),
                               [[2, 2, [0, 0]],
                                [1, 1, [1, 1]],
                                [2, 1, [1, 1]],
                                [3, 1, [1, 1]],
                                [1, 2, [1, 1]],
                                [3, 2, [1, 1]],
                                [1, 3, [1, 1]],
                                [2, 3, [1, 1]],
                                [3, 3, [1, 1]]])
        self.assertTrue(equal, "testCalculateValuesWithDispersion failed")
        equal = resultsEqualTest(self.__testRule.calculateValues(self.__cell2, self.__neighborhood2),
                               [[0, 0, [0, 0]],
                                [0, 1, [1, 1]],
                                [1, 1, [1, 1]],
                                [1, 0, [1, 1]]])
        self.assertTrue(equal, "testCalculateValuesWithDispersion failed")
        equal = resultsEqualTest(self.__testRule.calculateValues(self.__cell3, self.__neighborhood3),
                               [[2, 4, [0, 0]],
                                [1, 4, [1, 1]],
                                [1, 3, [1, 1]],
                                [2, 3, [1, 1]],
                                [3, 3, [1, 1]],
                                [3, 4, [1, 1]]])
        self.assertTrue(equal, "testCalculateValuesWithDispersion failed")