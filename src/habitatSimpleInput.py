# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# habitatSimpleInput.py
# Copyright (C) 2016 flossCoder
# 
# habitatSimpleInput.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# habitatSimpleInput.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package habitatSimpleInput defines an input based on CSV files. In addition to simpleInput one
# can read the habitat quality from a CSV file for each cell.

import csv

from constants import XINDEX, YINDEX
from simpleInput import SimpleInput
from zeroCA import zeroCA

## HabitatSimpleInput defines an input based on SimpleInput. In addition to SimpleInput, the
# habitat quality is read from CSV file for each cell.
class HabitatSimpleInput(SimpleInput):
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
    # @param qName name of the CSV file containing the quality of the hotbeds
    def __init__(self, coordinateTransformer, caInitName, directory, numx, numy, theta, m, r, qName):
        super().__init__(coordinateTransformer, caInitName, directory, numx, numy, theta, m, r, None)
        self.__qName = qName
        self.__quality = self.__loadQuality()
    
    
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
        if ((x < 0) | (x >= self._SimpleInput__numx) | (y < 0) | (y >= self._SimpleInput__numy)): # invalid index
            raise Exception("There is no entry with x = %i and y = %i." % (x, y))
        else:
            return (self._SimpleInput__values[0:3] + self.__quality[x][y])
    
    
    # private internal functions
    
    
    ## Load the quality of the hotbeds from a CSV file.
    #
    # @return the quality of the hotbeds
    def __loadQuality(self):
        quality = zeroCA(1, self._SimpleInput__numx, self._SimpleInput__numy)
        with open("%s/%s.csv" % (self._SimpleInput__directory, self.__qName), 'r', newline = "") as csvfile:
            data = csv.reader(csvfile, delimiter = ",")
            for dataRow in data:
                # dataRow contains the current row entry: x, y, quality of the hotbeds
                try:
                    coordinates = self._coordinateTransformer.calcInnerCoordinate(int(dataRow[XINDEX]),
                                                                                  int(dataRow[YINDEX]))
                    quality[coordinates[XINDEX]][coordinates[YINDEX]][0] = float(dataRow[2])
                except:
                    raise Exception("Input file contains invalid indices")
        return quality