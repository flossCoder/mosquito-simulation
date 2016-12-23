# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testRun.py
# Copyright (C) flossCoder
# 
# testRun.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testRun.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testRun
# This script is supposed to run the program for testing purpose.
# It should NOT be used otherwise.

from os import remove # needed to remove old CSV files
from constants import *
from setupRun import DIRECTORY
from simulationController import SimulationController

# basic variable set-up
a = 5 # size 5 x 5
width = a
height = a

directoryIn = "%s/input" % (DIRECTORY) # set directory for loading files
directoryOut = "%s/output" % (DIRECTORY) # set directory for loading files

transformerName = TESTTRANSFORMER

inputName = SIMPLEINPUT
inputArgs1 = {CAINITNAMEARGS:"initialCA1",
              DIRECTORYARGS:directoryIn,
              THETAARGS:22.0,
              MARGS:0.21,
              RARGS:3.25,
              QARGS:1.0}
inputArgs2 = {CAINITNAMEARGS:"initialCA2",
              DIRECTORYARGS:directoryIn,
              THETAARGS:22.0,
              MARGS:0.21,
              RARGS:3.25,
              QARGS:1.0}
inputArgs3 = {CAINITNAMEARGS:"initialCA3",
              DIRECTORYARGS:directoryIn,
              THETAARGS:22.0,
              MARGS:0.21,
              RARGS:3.25,
              QARGS:1.0}

caArgs = None
ruleArgs1 = {DISPERSIONARGS:False}
ruleArgs2 = {DISPERSIONARGS:True}

dataArgs1 = {NAMEARGS:"out1",
            DIRECTORYARGS:directoryOut}
dataArgs2 = {NAMEARGS:"out2",
             DIRECTORYARGS:directoryOut}
dataArgs3 = {NAMEARGS:"out3",
             DIRECTORYARGS:directoryOut}
dataArgs4 = {NAMEARGS:"out4",
             DIRECTORYARGS:directoryOut}
dataArgs5 = {NAMEARGS:"out5",
             DIRECTORYARGS:directoryOut}

# remove all existing output CSV data, if possible
try:
    remove("%s/%s.csv" % (directoryOut, dataArgs1[NAMEARGS]))
except:
    pass
try:
    remove("%s/%s.csv" % (directoryOut, dataArgs2[NAMEARGS]))
except:
    pass
try:
    remove("%s/%s.csv" % (directoryOut, dataArgs3[NAMEARGS]))
except:
    pass
try:
    remove("%s/%s.csv" % (directoryOut, dataArgs4[NAMEARGS]))
except:
    pass
try:
    remove("%s/%s.csv" % (directoryOut, dataArgs5[NAMEARGS]))
except:
    pass


# simple test without dispersion and easyCA
controller1 = SimulationController(width, height)
controller1.initTest(transformerName,
                     transformerName,
                     inputName,
                     COMBICA,
                     TESTRULE,
                     SIMPLEDATA,
                     inputArgs1,
                     caArgs,
                     ruleArgs1,
                     dataArgs1,
                     EASYCA)
controller1.doSimulation(1, 1)

# simple test with dispersion and easyCA
controller2 = SimulationController(width, height)
controller2.initTest(transformerName,
                     transformerName,
                     inputName,
                     COMBICA,
                     TESTRULE,
                     SIMPLEDATA,
                     inputArgs2,
                     caArgs,
                     ruleArgs2,
                     dataArgs2,
                     EASYCA)
controller2.doSimulation(1, 1)

# simple test without dispersion and stackCA
controller3 = SimulationController(width, height)
controller3.initTest(transformerName,
                     transformerName,
                     inputName,
                     COMBICA,
                     TESTRULE,
                     SIMPLEDATA,
                     inputArgs1,
                     caArgs,
                     ruleArgs1,
                     dataArgs3,
                     STACKCA)
controller3.doSimulation(1, 1)

# simple test with dispersion and stackCA for 10 days
controller4 = SimulationController(2 * width, 2 * height)
controller4.initTest(transformerName,
                     transformerName,
                     inputName,
                     COMBICA,
                     TESTRULE,
                     SIMPLEDATA,
                     inputArgs3,
                     caArgs,
                     ruleArgs2,
                     dataArgs4,
                     STACKCA)
controller4.doSimulation(10, 1)

# simple test with dispersion and stackCA for 10 days, save each third day
controller5 = SimulationController(2 * width, 2 * height)
controller5.initTest(transformerName,
                     transformerName,
                     inputName,
                     COMBICA,
                     TESTRULE,
                     SIMPLEDATA,
                     inputArgs3,
                     caArgs,
                     ruleArgs2,
                     dataArgs5,
                     STACKCA)
controller5.doSimulation(10, 4)

# just show a message, that the skript terminated
print("done")