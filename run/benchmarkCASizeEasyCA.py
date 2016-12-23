# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# benchmarkCASizeEasyCA.py
# Copyright (C) 2016 flossCoder
# 
# benchmarkCASizeEasyCA.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# benchmarkCASizeEasyCA.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package benchmarkCASizeEasyCA measures the timeEasyCA needed for a simulation step depending on the
# CA size. This test is done with the EasyCA and the MALCAM Rule.

import csv
from os import remove # needed to remove old CSV files
from time import clock

from constants import *
from setupRun import DIRECTORY
from simulationController import SimulationController

# basic variable set-up
directoryOut = "%s/benchmarkCA" % DIRECTORY # set directory for loading files

file = "%s/sizeTest.csv" % (directoryOut)

# existing output CSV data, if possible
try:
    remove(file)
except:
    pass

transformerName = TESTTRANSFORMER

inputName = SIMPLEINPUT
inputArgs1 = {CAINITNAMEARGS:"initialCA1",
              DIRECTORYARGS:None,
              THETAARGS:22.0,
              MARGS:0.21,
              RARGS:3.25,
              QARGS:1.0}

ruleArgs = {DISPERSIONARGS:True}

# measure the timeEasyCA for one timeEasyCA step depending on the CA size with easyCA
print("start measure timeEasyCA for one step depending on CA size")
with open(file, 'a', newline = '') as csvfile:
    data = csv.writer(csvfile, delimiter = ",")
    n = 1000000
    for l in range(1, 14):
        # set initial CA
        initCA = [[[1 for h in range(2)] for i in range(l)] for j in range(n)]
        # benchmarking with easyCA
        controller1 = SimulationController(n, l, False) # disable saving
        controller1.initBenchmark(transformerName,
                                  inputName,
                                  COMBICA,
                                  TESTRULE,
                                  inputArgs1,
                                  initCA,
                                  EASYCA,
                                  None,
                                  ruleArgs)
        timeEasyCA = clock()
        controller1.doSimulation(1, 1)
        timeEasyCA = clock() - timeEasyCA
        data.writerow([n * l, timeEasyCA])
        print("%i: number of cells: %i; timeEasyCA: %f" % (l, n * l, timeEasyCA))
print("measure timeEasyCA done")