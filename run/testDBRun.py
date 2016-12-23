# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testDBRun.py
# Copyright (C) 2016 flossCoder
# 
# testDBRun.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testDBRun.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testDBRun
# This script is supposed to run the program for testing purpose (especially the database).
# It should NOT be used otherwise. This script creates a new table.

from constants import *
from setupRun import DIRECTORY, DBNAME, USERNAME, HOST, PASSWORD, TESTTABLENAME
from simulationController import SimulationController

# Run dbtest to save the content of the database and remove the table if possible.
try:
    import dbtest
except:
    pass

# basic variable set-up
a = 10 # size 10 x 10
width = a
height = a

inputTransformerName = TESTTRANSFORMER
outputTransformerName = DBTRANSFORMER

inputName = SIMPLEINPUT
inputArgs1 = {CAINITNAMEARGS:"initialCA3",
              DIRECTORYARGS:"%s/input" % (DIRECTORY),
              THETAARGS:22.0,
              MARGS:0.21,
              RARGS:3.25,
              QARGS:1.0}

ruleName = TESTRULE
caArgs = None
ruleArgs1 = {DISPERSIONARGS:False}
ruleArgs2 = {DISPERSIONARGS:True}

dataName = DBDATA
dataArgs = {NAMEARGS:TESTTABLENAME,
            DBNAMEARGS:DBNAME,
            USERARGS:USERNAME,
            HOSTARGS:HOST,
            PASSWORDARGS:PASSWORD,
            NEWTABLEARGS:True,
            WIDTHARGS:width,
            HEIGHTARGS:height,
            UPPERLEFTXARGS:0.0005,
            UPPERLEFTYARGS:0.0005,
            SCALEXARGS:1,
            SCALEYARGS:1,
            SKEWXARGS:0,
            SKEWYARGS:0,
            SRIDARGS:SRIDUNKNOWN}

controller1 = SimulationController(width, height)
controller1.initTest(inputTransformerName,
                     outputTransformerName,
                     inputName,
                     COMBICA,
                     ruleName,
                     dataName,
                     inputArgs1,
                     caArgs,
                     ruleArgs2,
                     dataArgs,
                     STACKCA)
controller1.doSimulation(1, 1)

# just show a message, that the skript terminated
print("done")