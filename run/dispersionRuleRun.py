# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# dispersionRuleRun.py
# Copyright (C) 2016 flossCoder
# 
# dispersionRuleRun.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# dispersionRuleRun.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package dispersionRuleRun
# This script is supposed to run the program for testing purpose.
# It should NOT be used otherwise.

from os import remove # needed to remove old CSV files
from constants import *
from setupRun import DIRECTORY
from simulationController import SimulationController

# basic variable set-up
a = 10 # size 10 x 10
width = a
height = a

directoryIn = "%s/input" % (DIRECTORY) # set directory for loading files
directoryOut = "%s/output" % (DIRECTORY) # set directory for loading files

transformerName = TESTTRANSFORMER

inputName = HABITATSIMPLEINPUT
inputArgs = {CAINITNAMEARGS:"initialCA4",
             DIRECTORYARGS:directoryIn,
             THETAARGS:22.0,
             MARGS:0.21,
             RARGS:3.25,
             QNAMEARGS:"initialQuality1"}

caArgs = None
ruleArgs = {AREAARGS:2500, # assume 50 m x 50 m area
            MOVINGFACTORARGS:0.2}

dataArgs = {NAMEARGS:"dispersion1",
            DIRECTORYARGS:directoryOut}

# remove all existing output CSV data, if possible
try:
    remove("%s/%s.csv" % (directoryOut, dataArgs[NAMEARGS]))
except:
    pass

# simple test without dispersion and easyCA
controller1 = SimulationController(width, height)
controller1.initTest(transformerName,
                     transformerName,
                     inputName,
                     COMBICA,
                     DISPERSIONRULE,
                     SIMPLEDATA,
                     inputArgs,
                     caArgs,
                     ruleArgs,
                     dataArgs,
                     None)
controller1.doSimulation(100, 1)

print("done")