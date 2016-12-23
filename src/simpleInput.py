# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# simpleInput.py
# Copyright (C) 2016 flossCoder
# 
# simpleInput.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# simpleInput.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package simpleInput defines an input based on CSV files.

import csv
from abstractInput import AbstractInput
from constants import XINDEX, YINDEX
from zeroCA import zeroCA

## SimpleInput defines a data input based on CSV-Files for testing purpose and easy to handle
# simulations.
class SimpleInput(AbstractInput):
    ## init function
    #
    # @param coordinateTransformer can transform the internal indexes to real coordinates (used
    # by GIS for example) and vice versa
    # @param caInitName file name for loading the initial state
    # @param directory storage for the files
    # @param numx number of cells in abscissa
    # @param numy number of cells in ordinate
    # @param theta temperature in degree celsius
    # @param m mortality rate for the adults
    # @param r reproduction rate for the adults
    # @param q quality of the hotbeds
    def __init__(self, coordinateTransformer, caInitName, directory, numx, numy, theta, m, r, q):
        super().__init__(coordinateTransformer)
        self.__caInitName = caInitName
        self.__directory = directory
        self.__numx = numx
        self.__numy = numy
        # self.__values contains the values which can be returned by getValuesOfCell
        # temperature in degree celsius       theta 0
        # mortality rate for the adults       m     1
        # reproduction rate for the adults    r     2
        # quality of the hotbeds              q     3
        self.__values = [theta, m, r, q]
    
    
    # getter functions
    
    
    ## gather the data for the given cell
    #
    # @param day of simulation
    # @param cell index which is needed, format [x, y]
    #
    # @return a list with the values of the cell
    #
    # @exception the given cell is invalid
    def getDataOfCell(self, day, cell):
        x = cell[XINDEX]
        y = cell[YINDEX]
        if ((x < 0) | (x >= self.__numx) | (y < 0) | (y >= self.__numy)): # invalid index
            raise Exception("There is no entry with x = %i and y = %i." % (x, y))
        else:
            return self.__values
    
    ## returns the initial state of the cellular automata
    #
    # @return an array containing abscissa, ordinate, adults and larvae
    #
    # @exception if the input file contains invalid indices
    def getInitialState(self):
        initialState = zeroCA(2, self.__numx, self.__numy)
        # open the init file
        with open("%s/%s.csv" % (self.__directory, self.__caInitName), 'r', newline = "") as csvfile:
            data = csv.reader(csvfile, delimiter = ",")
            for initialRow in data:
                # initialRow contains the current row entry: x, y, number of mosquitos and larvae
                try:
                    coordinates = self._coordinateTransformer.calcInnerCoordinate(int(initialRow[XINDEX]),
                                                                                  int(initialRow[YINDEX]))
                    initialState[coordinates[XINDEX]][coordinates[YINDEX]][0] = int(initialRow[2])
                    initialState[coordinates[XINDEX]][coordinates[YINDEX]][1] = int(initialRow[3])
                except:
                    raise Exception("Input file contains invalid indices")
        return initialState
                