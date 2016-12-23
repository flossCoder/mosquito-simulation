# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testSuite.py
# Copyright (C) 2016 flossCoder
# 
# testSuite.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testSuite.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testSuite for running all test cases.

import unittest

from testAbstractMatrix import TestAbstractMatrix
from testCombiCA import TestCombiCA
from testDBData import TestDBData
from testDBTransformer import TestDBTransformer
from testEasyCA import TestEasyCA
from testHabitatSimpleInput import TestHabitatSimpleInput
from testIntegration import TestIntegration
from testSimpleData import TestSimpleData
from testSimpleInput import TestSimpleInput
from testStackCA import TestStackCA
from testTestRule import TestTestRule
from testTestTransformer import TestTestTransformer

## Define a test suite, which aggregates all unit tests.
class TestSuite(unittest.TestSuite):
    def suite(self):
        # test the simulation core
        self.addTest(TestAbstractMatrix)
        self.addTest(TestCombiCA)
        self.addTest(TestEasyCA)
        self.addTest(TestStackCA)
        
        # test the used rules
        self.addTest(TestTestRule)
        
        # test the transformer
        self.addTest(TestDBTransformer)
        self.addTest(TestTestTransformer)
        
        # test the input
        self.addTest(TestSimpleInput)
        self.addTest(TestHabitatSimpleInput)
        
        # test the data output
        self.addTest(TestSimpleData)
        self.addTest(TestDBData)
        
        # test the whole system: Especially the SimulationController and the interaction
        # between the components are tested using SimpleInput, SimpleData, TestTransformer
        # and TestRule).
        self.addTest(TestIntegration)