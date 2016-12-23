# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# helper.py
# Copyright (C) 2016 flossCoder
# 
# helper.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# helper.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package helper gathers functionalities with are needed for testing but should not be used
# otherwise.

import csv

## Helping function to load the init state of a CA from a CSV file.
#
# @param directory of the CSV file to load
# @param name of the CSV file to load
# @param numx number of cells on abscissa
# @param numy number of cells on ordinate
def loadInitState(directory, name, numx = 5, numy = 5):
    step = getZero(numx, numy)
    with open("%s/%s.csv" % (directory, name), 'r', newline = '') as csvfile:
        data = csv.reader(csvfile, delimiter = ",")
        for row in data:
            step[int(row[0])][int(row[1])][0] = int(row[2]) # adults
            step[int(row[0])][int(row[1])][1] = int(row[3]) # larvae
    return step

## Helping function to save a CA to CSV file.
#
# @param ca to save
# @param day of simulation to save
# @param directory where the CSV file will be saved
# @param name of the CSV file
def saveCA(ca, day, directory, name):
    with open("%s/%s.csv" % (directory, name), 'a', newline = '') as csvfile:
            data = csv.writer(csvfile, delimiter = ",")
            for i in range(len(ca)):
                for j in range(len(ca[i])):
                    data.writerow([day, # day
                                   i, # first coordinate
                                   j, # second coordinate
                                   ca[i][j][0], # adults
                                   ca[i][j][1] # larvae
                                   ])

## Helping function to load a CA from a CSV file.
#
# @param directory of the CSV file to load
# @param name of the CSV file to load
# @param day of simulation to load
# @param numx number of cells on abscissa
# @param numy number of cells on ordinate
def loadCA(directory, name, day = 0, numx = 5, numy = 5):
    step = getZero(numx, numy)
    with open("%s/%s.csv" % (directory, name), 'r', newline = '') as csvfile:
        data = csv.reader(csvfile, delimiter = ",")
        for row in data:
            if (int(row[0]) == day): # correct day
                step[int(row[1])][int(row[2])][0] = int(row[3]) # adults
                step[int(row[1])][int(row[2])][1] = int(row[4]) # larvae
    return step

## Function getComparator5x5 returns a list with following entries:
#       0       1       2       3
# 0: [0, 0], [1, 1], [0, 0], [0, 0]
# 1: [0, 0], [0, 0], [0, 0], [0, 0]
# 2: [0, 0], [0, 0], [1, 1], [0, 0]
# 3: [0, 0], [0, 0], [0, 0], [1, 1]
# 4: [0, 0], [0, 0], [0, 0], [0, 0]
def getComparator5x4():
    comparator = getZero(5, 4)
    comparator[0][1] = [1, 1]
    comparator[2][2] = [1, 1]
    comparator[4][3] = [1, 1]
    return comparator

## Function getZero calculates a zero list with the given dimension.
#
# @param numx number of cells on abscissa
# @param numy number of cells on ordinate
#
# @return a zero numx * numy * 2 list
def getZero(numx, numy):
    return [[[0 for h in range(2)] for i in range(numy)] for j in range(numx)]

## Test if the two given results returned by a call of calculateValues from a rule are equal.
#
# @param result1 first list
# @param result2 second list
#
# @return True: results are equal; False: results are not equal
def resultsEqualTest(result1, result2):
    if (len(result1) != len(result2)):
        return False
    for i in range(len(result1)):
        if not(listsEqualTest(result1[i], result2[i])):
            return False
    return True

## Helping function to test, if two given lists are equal (just to make the code of the
# testMooreNeighborhood function a little bit nicer to read).
#
# @param list1 the fist list
# @param list2 the second list
#
# @return equal = True: lists are equal; equal = False: lists are not equal
def listsEqualTest(list1, list2):
    equal = True
    # Test if each element i in list1 is in list2.
    if ([i for i in list1 if i not in list2] != []):
        # There are elements i in list1, which are not in list2.
        # => list1 and list2 are not equal
        equal = False
    # Test if each element i in list2 is in list1.
    if ([i for i in list2 if i not in list1] != []):
        # There are elements i in list2, which are not in list1.
        # => list1 and list2 are not equal
        equal = False
    return equal

## PseudoController is needed, to test several components independent of the SimulationController
# and the CombiCA.
# DO NOT USE THIS CLASS FOR OTHER PURPOSE THEN TESTING!!!
class PseudoController():
    ## Init function.
    #
    # @param rule the rule to calculate the simulation step.
    def __init__(self, rule = None):
        self.rule = rule
    
    ## get the data for the simulation of the given cells for the given day
    #
    # @param cell which is needed, format [x, y]
    #
    # @return required data are []
    def getDataOfCell(self, cell):
        return [cell[0], cell[1], []]
    
    ## This function helps to simulate the CombiCA. The function calls the rule to calculate the
    # new state.
    #
    # @param cell to calculate, format [x, y, adults, larvae, theta, m, r, q]
    # @param neighourhood of the cell to calculate, format
    #                     [[x0, y0, adults, larvae, theta0, m0, r0, q0], ...]
    #
    # @return new state of the given cells, format [[x, y, adults, larvae], ...]
    def calculateValues(self, cell, neighborhood):
        return self.rule.calculateValues(cell, neighborhood)