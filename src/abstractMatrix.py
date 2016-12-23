# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-
#
# abstractMatrix.py
# Copyright (C) 2016 flossCoder
#
# abstractMatrix.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# abstractMatrix.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package abstractMatrix defines the data structure for EasyCA and StackCA.

from constants import XINDEX, YINDEX, STATEINDEX
from zeroCA import zeroCA

## AbstractMatrix defines the data structure plus some operations for EasyCA and StackCA.
class AbstractMatrix(object):
    ## initialize the CA data structure
    #
    # @param combiCA needed for communication
    # @param numx the number of cells on the abscissa
    # @param numy the number of cells on the ordinate
    # @param initCA the initial CA
    #
    # @exception invalid size of the given CA.
    def __init__(self, combiCA, numx, numy, initCA):
        if ((len(initCA) != numx) | (len(initCA[0]) != numy)):
            raise Exception("The given CA has an invalid size.")
        self._combiCA = combiCA
        self._numx = numx
        self._numy = numy
        # set up the cellular automaton
        self.__length = len(initCA[0][0]) # how many parameter are given?
        self._matrixA = zeroCA(self.__length, self._numx, self._numy)
        self._matrixB = initCA
        self.__useA = True # true: write in matrixA, false: write in matrixB
    
    
    # public functions (interfaces for the environment)
    
    
    ## doStep performs one simulation step.
    def doStep(self):
        # Do the calculation.
        self._performCalculation()
        # At the end of the step toggle the usage of the current matrix.
        self._toggleUseA()
    
    
    # getter functions
    
    
    ## Helping function to return the state of the last simulation step.
    # It has to be returned the CA which is not pointed by self.__useA, because the one pointed
    # by self.__useA will be written during the next doStep call. That means a zero matrix would
    # be returned.
    #
    # @return the current matrix
    def getCA(self):
        if not(self.__useA):
            return self._matrixA
        else:
            return self._matrixB
    
    ## get the state of the given cell of the previous step
    #
    # @param cell index which is needed, format [x, y]
    #
    # @return cell (x, y) of the previous time step
    def _getOldCell(self, cell):
        if (self.__useA):
            return self._matrixB[cell[XINDEX]][cell[YINDEX]]
        else:
            return self._matrixA[cell[XINDEX]][cell[YINDEX]]
    
    ## get the data for the simulation of the given cells
    #
    # @param cells indexes are needed
    #
    # @return required data plus the CA state of the previous time step
    def _getDataOfCells(self, cells):
        result = []
        for cell in cells:
            result.append([cell[XINDEX], cell[YINDEX],
                           self._getOldCell(cell), self._combiCA.getDataOfCell(cell)])
        return result
    
    ## Getter for the flag of the used matrix.
    #
    # @return useA: true: write in matrixA, false: write in matrixB
    def _getUseA(self):
        return self.__useA
    
    
    # setter functions
    
    
    ## setCA is needed for initialization and loading a saved state 
    #
    # @param CA to use
    #
    # @exception invalid size of the given CA
    def setCA(self, ca):
        if ((self._numx != len(ca)) | (self._numy != len(ca[XINDEX]))):
            raise Exception("The given CA has an invalid size.")
        elif self.__useA:
            self._matrixB = ca
        else:
            self._matrixA = ca
    
    
    # protected functions (can be used from derivative classes)
    
    
    ## helping function to change the state of useA and reset the matrix which will be used next
    def _toggleUseA(self):
        if self.__useA: # matrixA is the current matrix
            # reset matrixB
            self._matrixB = zeroCA(self.__length, self._numx, self._numy)
        else: # matrixB is the current matrix
            # reset matrixA
            self._matrixA = zeroCA(self.__length, self._numx, self._numy)
        self.__useA = not(self.__useA)
    
    ## Perform the calculation of the step.
    #
    # @exception NotImplementedError forces one to implement this function
    def _performCalculation(self):
        raise NotImplementedError("performCalculation has not yet been implemented")
    
    ## Do simulation of the current cell with Moore Neighborhood.
    # What is the "current cell" must be implemented in doStep by inheriting class.
    #
    # @param cell index of cell to simulate, format [x, y]
    def _simulateCurrentCell(self, cell):
        # First off all gather the required information of the cells (state and input data for
        # the given cell plus the neighbor cells.
        # get simulation data for the current cell
        dataCurrentCell = self._getDataOfCells([cell])
        # get simulation data for the Moore neighborhood
        dataNeighborCells = self._getDataOfCells(self._mooreNeighborhood(cell))
        
        # perform calculation for cell
        result = self._calculateValues(dataCurrentCell[0], dataNeighborCells)
        
        # update cells of the current matrix
        self._updateValuesOfCells(result)
    
    ## calculates a list of indexes for the Moore neighbors of the given cell using mirroring for
    # boundary conditions
    #
    # @param cell index, format [x, y]
    #
    # @return index list of neighbors
    def _mooreNeighborhood(self, cell):
        x = cell[XINDEX]
        y = cell[YINDEX]
        neighborCells = []
        # for saving some calculations
        xmax = self._numx - 1
        ymax = self._numy - 1
        xm = x - 1
        xp = x + 1
        ym = y - 1
        yp = y + 1
        
        if (x > 0):
            neighborCells.append([xm, y])
            if (y < ymax):
                neighborCells.append([xm, yp])
            if (y > 0):
                neighborCells.append([xm, ym])
        if (x < xmax):
            neighborCells.append([xp, y])
            if (y < ymax):
                neighborCells.append([xp, yp])
            if (y > 0):
                neighborCells.append([xp, ym])
        
        if (y < ymax):
            neighborCells.append([x, yp])
        if (y > 0):
            neighborCells.append([x, ym])
        
        return neighborCells
    
    ## Update the given cells.
    #
    # @param cells indexes to update, format [[x0, y0, [adults0, larvae0]], ...]
    def _updateValuesOfCells(self, cells):
        for cell in cells:
            self._updateValuesOfCell(cell)
    
    ## Update the given cell. Update means x = x + givenCell. This must be done for being able
    # to handle dispersion correctly.
    #
    # @param cell in format [x, y, [adults, larvae]]
    def _updateValuesOfCell(self, cell):
        for i in range(len(cell[STATEINDEX])):
            # update state for each entry
            if self.__useA:
                self._matrixA[cell[XINDEX]][cell[YINDEX]][i] += cell[STATEINDEX][i]
            else:
                self._matrixB[cell[XINDEX]][cell[YINDEX]][i] += cell[STATEINDEX][i]
    
    ## This function implements the calculation of the values.
    #
    # @param cell to calculate, format [x, y, adults, larvae, theta, m, r, q]
    # @param neighorhood of the cell to calculate, format
    #                     [[x0, y0, adults, larvae, theta0, m0, r0, q0], ...]
    #
    # @return new state of the given cells, format [[x, y, adults, larvae], ...]
    def _calculateValues(self, cell, neighborhood):
        return self._combiCA.calculateValues(cell, neighborhood)