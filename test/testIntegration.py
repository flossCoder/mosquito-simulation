# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testIntegration.py
# Copyright (C) 2016 flossCoder
# 
# testIntegration.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testIntegration.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testIntegration contains the integration test.

from os import remove
import unittest

from constants import *
from helper import loadCA, loadInitState, listsEqualTest, getZero
from setupTests import DIRECTORY
from simulationController import SimulationController

## Class TestIntegration defines a full integration test (using SimpleInput, SimpleData,
# TestTransformer and TestRule) of the whole system. Especially the SimulationController
# and the interaction between the components is tested.
class TestIntegration(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        # Set up the needed variables.
        self.__width = 5
        self.__hight = 4
        
        self.__transformerName = TESTTRANSFORMER
        
        self.__inputArgs = {CAINITNAMEARGS:"testCA",
                            DIRECTORYARGS:DIRECTORY,
                            THETAARGS:22,
                            MARGS:1.5,
                            RARGS:2.0,
                            QARGS:1.0}
        
        self.__ruleArgs1 = {DISPERSIONARGS:False}
        self.__ruleArgs2 = {DISPERSIONARGS:True}
        
        self.__dataArgs = {NAMEARGS:"out",
                           DIRECTORYARGS:DIRECTORY}
        self.__simulationController = SimulationController(self.__width, self.__hight)
    
    ## Finish the test: remove the out.csv file.
    def tearDown(self):
        # remove the csv file
        try:
            remove("%s/%s.csv" % (self.__dataArgs[DIRECTORYARGS], self.__dataArgs[NAMEARGS]))
        except:
            pass
    
    ## Test the initialization and simulation of the EasyCA with the TestRule without dispersion.
    def testEasyCAWithoutDispersion(self):
        self.__simulationController.initTest(self.__transformerName,
                                             self.__transformerName,
                                             SIMPLEINPUT,
                                             COMBICA,
                                             TESTRULE,
                                             SIMPLEDATA,
                                             self.__inputArgs,
                                             None, # caArgs
                                             self.__ruleArgs1,
                                             self.__dataArgs,
                                             EASYCA)
        self.__simulationController.doSimulation(1, 1) # do one step, save each step
        state = [[[1000, 100] for i in range(self.__hight)] for j in range(self.__width)]
        state[0][1] = [1001, 101]
        state[2][2] = [1001, 101]
        state[4][3] = [1001, 101]
        self.__simulationTest(state, "testEasyCAWithoutDispersion")
        
    ## Test the initialization and simulation of the EasyCA with the TestRule with dispersion.
    def testEasyCAWithDispersion(self):
        self.__simulationController.initTest(self.__transformerName,
                                             self.__transformerName,
                                             SIMPLEINPUT,
                                             COMBICA,
                                             TESTRULE,
                                             SIMPLEDATA,
                                             self.__inputArgs,
                                             None, # caArgs
                                             self.__ruleArgs2,
                                             self.__dataArgs,
                                             EASYCA)
        self.__simulationController.doSimulation(1, 1) # do one step, save each step
        state = getZero(self.__width, self.__hight)
        state[0][0] = [3, 3]
        state[0][1] = [6, 6]
        state[0][2] = [5, 5]
        state[0][3] = [3, 3]
        state[1][0] = [5, 5]
        state[1][1] = [8, 8]
        state[1][2] = [8, 8]
        state[1][3] = [5, 5]
        state[2][0] = [5, 5]
        state[2][1] = [8, 8]
        state[2][2] = [9, 9]
        state[2][3] = [5, 5]
        state[3][0] = [5, 5]
        state[3][1] = [8, 8]
        state[3][2] = [8, 8]
        state[3][3] = [5, 5]
        state[4][0] = [3, 3]
        state[4][1] = [5, 5]
        state[4][2] = [5, 5]
        state[4][3] = [4, 4]
        self.__simulationTest(state, "testEasyCAWithDispersion")
    
    ## Test the initialization and simulation of the StackCA with the TestRule without dispersion.
    def testStackCAWighoutDispersion(self):
        self.__simulationController.initTest(self.__transformerName,
                                             self.__transformerName,
                                             SIMPLEINPUT,
                                             COMBICA,
                                             TESTRULE,
                                             SIMPLEDATA,
                                             self.__inputArgs,
                                             None, # caArgs
                                             self.__ruleArgs1,
                                             self.__dataArgs,
                                             STACKCA)
        self.__simulationController.doSimulation(1, 1) # do one step, save each step
        state = getZero(self.__width, self.__hight)
        state[0][1] = [1001, 101]
        state[2][2] = [1001, 101]
        state[4][3] = [1001, 101]
        self.__simulationTest(state, "testStackCAWighoutDispersion")
    
    ## Test the initialization and simulation of the StackCA with the TestRule with dispersion.
    def testStackCAWithDispersion(self):
        self.__simulationController.initTest(self.__transformerName,
                                             self.__transformerName,
                                             SIMPLEINPUT,
                                             COMBICA,
                                             TESTRULE,
                                             SIMPLEDATA,
                                             self.__inputArgs,
                                             None, # caArgs
                                             self.__ruleArgs2,
                                             self.__dataArgs,
                                             STACKCA)
        self.__simulationController.doSimulation(1, 1) # do one step, save each step
        state = getZero(self.__width, self.__hight)
        state[0][0] = [1, 1]
        state[0][1] = [1, 1]
        state[0][2] = [1, 1]
        state[1][0] = [1, 1]
        state[1][1] = [2, 2]
        state[1][2] = [2, 2]
        state[1][3] = [1, 1]
        state[2][1] = [1, 1]
        state[2][2] = [1, 1]
        state[2][3] = [1, 1]
        state[3][1] = [1, 1]
        state[3][2] = [2, 2]
        state[3][3] = [2, 2]
        state[4][2] = [1, 1]
        state[4][3] = [1, 1]
        self.__simulationTest(state, "testStackCAWithDispersion")
    
    ## This function tests, if the initial state and the state after one simulation step have
    # been saved correctly.
    #
    # @param state after one simulation step
    # @param name of the test (will be printed to console, if a test fails)
    def __simulationTest(self, state, name):
        equal = listsEqualTest(loadCA(self.__dataArgs[DIRECTORYARGS],
                                      self.__dataArgs[NAMEARGS],
                                      0, # day 0 => initial state
                                      self.__width,
                                      self.__hight),
                               loadInitState(self.__inputArgs[DIRECTORYARGS],
                                             self.__inputArgs[CAINITNAMEARGS],
                                             self.__width,
                                             self.__hight))
        self.assertTrue(equal, "%s (initial state) failed" % name) # check initial state
        equal = listsEqualTest(loadCA(self.__dataArgs[DIRECTORYARGS],
                                      self.__dataArgs[NAMEARGS],
                                      1,
                                      self.__width,
                                      self.__hight),
                               state)
        self.assertTrue(equal, "%s (after one step) failed" % name) # check initial state