# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testSimpleData.py
# Copyright (C) 2016 flossCoder
# 
# testSimpleData.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testSimpleData.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testSimpleData for testing the simpleData.

from os import remove
import unittest

from helper import listsEqualTest, getComparator5x4, loadCA, saveCA
from setupTests import DIRECTORY
from simpleData import SimpleData
from testTransformer import TestTransformer


## Test the SimpleData class.
class TestSimpleData(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        self.__name = "testOut"
        self.__coordinateTransformer = TestTransformer()
        self.__directory = DIRECTORY
        self.__simpleData = SimpleData(self.__name,
                                         self.__coordinateTransformer,
                                         self.__directory)
        # set up data structure needed for the following tests
        self.__ca = getComparator5x4()
    
    ## Finish the test: Remove the testOut.csv file.
    def tearDown(self):
        remove("%s/%s.csv" % (self.__directory, self.__name)) # remove the CSV file
    
    ## Test the saveStep function with self.__ca.
    def testSaveStep(self):
        self.__simpleData.saveStep(self.__ca, 0)
        equal = listsEqualTest(self.__ca, loadCA(self.__directory, self.__name, 0, 5, 4))
        self.assertTrue(equal, "testSaveStep failed")
    
    ## Test the loadStep function with self.__ca.
    def testLoadStep(self):
        saveCA(self.__ca, 0, self.__directory, self.__name) # save the CA
        equal = listsEqualTest(self.__simpleData.loadStep(0, 5, 4), self.__ca)
        self.assertTrue(equal, "testLoadStep failed")