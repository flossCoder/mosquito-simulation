# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# benchmarkCAFillingDegree.py
# Copyright (C) 2016 flossCoder
# 
# benchmarkCAFillingDegree.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# benchmarkCAFillingDegree.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package benchmarkCAFillingDegree measures the time needed for a simulation step depending on
# the filling degree of the CA. This test compares EasyCA and StackCA with the MALCAM Rule.

import csv
from os import remove
from time import clock

from constants import *
from setupRun import DIRECTORY
from simulationController import SimulationController

# basic variable set-up
directoryOut = "%s/benchmarkCA" % (DIRECTORY) # set directory for loading files

transformerName = TESTTRANSFORMER

inputName = SIMPLEINPUT
inputArgs1 = {CAINITNAMEARGS:"initialCA1",
              DIRECTORYARGS:None,
              THETAARGS:22.0,
              MARGS:0.21,
              RARGS:3.25,
              QARGS:1.0}

ruleArgs = {DISPERSIONARGS:True}

width = 1000
height = 1000
step = 50 # number of filled entries per step
numberSimSteps = 1 # number of simulation steps

file = "%s/fillingDegreeTest_%i_%i.csv" % (directoryOut, width * height, numberSimSteps)

# remove old file with results, if possible
try:
    remove(file)
except:
    pass

# measure the timeEasyCA for one timeEasyCA step depending on the CA size with easyCA
print("start measure time for one step depending on CA filling degree")
with open(file, 'a', newline = '') as csvfile:
    data = csv.writer(csvfile, delimiter = ",")
    # set initial CA
    initCA = [[[0 for h in range(2)] for i in range(height)] for j in range(width)]
    for fill in range(0, 951, step):
        for l in range(step):
            initCA[(fill + l)] = [[42 for h in range(2)] for i in range(height)] # set cells to != 0
        # benchmarking with easyCA
        controller1 = SimulationController(width, height, False) # disable saving
        controller1.initBenchmark(transformerName,
                                  inputName,
                                  COMBICA,
                                  TESTRULE,
                                  inputArgs1,
                                  initCA,
                                  EASYCA,
                                  ruleArgs)
        timeEasyCA = clock()
        controller1.doSimulation(numberSimSteps, 1)
        timeEasyCA = clock() - timeEasyCA
        
        # benchmarking with stackCA
        controller2 = SimulationController(width, height, False) # disable saving
        controller2.initBenchmark(transformerName,
                                  inputName,
                                  COMBICA,
                                  TESTRULE,
                                  inputArgs1,
                                  initCA,
                                  STACKCA,
                                  ruleArgs)
        timeStackCA = clock()
        controller2.doSimulation(numberSimSteps, 1)
        timeStackCA = clock() - timeStackCA
        
        data.writerow([(fill + step) * height, timeEasyCA, timeStackCA])
        print("filled cells: %i timeEasyCA: %f timeStackCA: %f" % ((fill + step) * height,
                                                                   timeEasyCA, timeStackCA))
print("measure time done")