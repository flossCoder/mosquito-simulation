# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# simpleData.py
# Copyright (C) 2016 flossCoder
# 
# simpleData.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# simpleData.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package simpleData defines an output based on CSV files.

import csv
from abstractData import AbstractData
from constants import TYPECSV, XINDEX, YINDEX
from zeroCA import zeroCA

## SimpleData defines a CA saving based on CSV-files
class SimpleData(AbstractData):
    ## init function
    #
    # @param name of the data, will be used as a filename
    # @param coordinateTransformer can transform the internal indexes to real coordinates (used
    # by GIS for example) and vice versa
    # @param directory the directory where the file should be saved
    def __init__(self, name, coordinateTransformer, directory):
        super().__init__(TYPECSV, name, coordinateTransformer)
        self.__directory = directory
    
    
    # public functions (interfaces for the environment)
    
    
    ## Save the given step to all registered elements.
    #
    # @param ca to save
    # @param day to save
    def saveStep(self, ca, day):
        with open("%s/%s.csv" % (self.__directory, self._name), 'a', newline = '') as csvfile:
            data = csv.writer(csvfile, delimiter = ",")
            for i in range(len(ca)):
                for j in range(len(ca[i])):
                    coordinates = self._coordinateTransformer.calcOuterCoordinate(i, j)
                    data.writerow([day, # day
                                   coordinates[XINDEX], # first coordinate
                                   coordinates[YINDEX], # second coordinate
                                   ca[i][j][0], # adults
                                   ca[i][j][1] # larvae
                                   ])
    
    ## Open a simulation step.
    #
    # @param day of simulation to load
    # @param numx number of cells on abscissa
    # @param numy number of cells on ordinate
    #
    # @return the state of the CA on the given day
    #
    # @exception invalid given day
    def loadStep(self, day, numx, numy):
        step = zeroCA(2, numx, numy)
        opened = False # did a row of the CSV file fit to the given day?
        with open("%s/%s.csv" % (self.__directory, self._name), 'r', newline = '') as csvfile:
            data = csv.reader(csvfile, delimiter = ",")
            for row in data:
                coordinates = self._coordinateTransformer.calcInnerCoordinate(int(row[1]),
                                                                             int(row[2]))
                if (int(row[0]) == day): # correct day
                    step[coordinates[XINDEX]][coordinates[YINDEX]][0] = int(row[3]) # adults
                    step[coordinates[XINDEX]][coordinates[YINDEX]][1] = int(row[4]) # larvae
                    opened = True
                if (opened & (int(row[0]) != day)):
                    # found the end of the interesting part
                    break
        if not(opened): # no row of the CSV file fitted to the given day
            raise Exception("No entries for day = %i." % (day))
        return step