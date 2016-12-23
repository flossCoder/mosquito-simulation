# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# applicationTest.py
# Copyright (C) 2016 flossCoder
# 
# applicationTest.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# applicationTest.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package applicationTest runs the system for a long time with a big CA.

from os import remove # needed to remove old CSV files

from constants import *
from setupRun import DIRECTORY
from simulationController import SimulationController

# basic variable set-up
a = 1000 # size 5 x 5
width = a
height = a

directoryIn = "%s/input" % (DIRECTORY) # set directory for loading files
directoryOut = "%s/applicationTest" % (DIRECTORY) # set directory for loading files

transformerName = TESTTRANSFORMER

inputName = HABITATSIMPLEINPUT
inputArgs1 = {CAINITNAMEARGS:"initialCA5",
              DIRECTORYARGS:directoryIn,
              THETAARGS:25.0,
              MARGS:0.21,
              RARGS:3.25,
              QNAMEARGS:"initialQuality2"}

dataArgs1 = {NAMEARGS:"functionality1",
            DIRECTORYARGS:directoryOut}

ruleArgs = {AREAARGS:2500, # assume 50 m x 50 m area
            MOVINGFACTORARGS:0.2}

# remove all existing output CSV data, if possible
try:
    remove("%s/%s.csv" % (directoryOut, dataArgs1[NAMEARGS]))
except:
    pass

controller1 = SimulationController(width, height)
controller1.initTest(transformerName,
                     transformerName,
                     inputName,
                     COMBICA,
                     DISPERSIONRULE,
                     SIMPLEDATA,
                     inputArgs1,
                     None,
                     ruleArgs,
                     dataArgs1,
                     None)
controller1.doSimulation(100, 10)

# just show a message, that the skript terminated
print("done")