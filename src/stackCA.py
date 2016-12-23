# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# stackCA.py
# Copyright (C) 2016 flossCoder
# 
# stackCA.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# stackCA.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package stackCA implements the stack method.

from abstractMatrix import AbstractMatrix
from constants import XINDEX, YINDEX, STATEINDEX

## StackCA implements the stack method, which is good for sparse CA.
class StackCA(AbstractMatrix):
    ## initialize the data structure
    #
    # @param combiCA needed for communication
    # @param numx the number of cells on the abscissa
    # @param numy the number of cells on the ordinate
    # @param initCA the initial CA
    def __init__(self, combiCA, numx, numy, initCA):
        super().__init__(combiCA, numx, numy, initCA)
        self.__stackP = []
        self.__stackQ = []
        self.__useP = True # true: read from stackP, false: read from stackQ
        self.__fillStack()
    
    
    # public functions (interfaces for the environment)
    
    
    ## Get the size of the stack, which represents the number of filled cells.
    #
    # @return the number of elements of the stack
    def getSizeOfStack(self):
        if (self.__useP):
            return len(self.__stackP)
        else:
            return len(self.__stackQ)
    
    
    # protected functions (can be used from derivative classes)
    
    
    ## doStep performs one simulation step
    def _performCalculation(self):
        if(self.__useP): # read stackP
            while (self.__stackP): # stackP is not empty
                index = self.__stackP.pop()
                self._simulateCurrentCell(index)
        else: # read stackQ
            while (self.__stackQ): # stackQ is not empty
                index = self.__stackQ.pop()
                self._simulateCurrentCell(index)
        
        # At the end of the step toggle the current stack.
        self.__useP = not(self.__useP)
    
    
    ## Update the given cell. Update means x = x + givenCell. This must be done for being able
    # to handle dispersion correctly.
    #
    # @param cell in format [x, y, [adults, larvae]]
    def _updateValuesOfCell(self, cell):
        newStateIsEmpty = True
        oldStateIsEmpty = True
        for i in range(len(cell[STATEINDEX])):
            # check, whether the old state of the given cell is empty or not
            if (cell[STATEINDEX][i] != 0):
                newStateIsEmpty = False
            
            # update state for each entry
            if self._getUseA():
                # check, whether the old state of the given cell is empty or not
                if (self._matrixA[cell[XINDEX]][cell[YINDEX]][i] != 0):
                    oldStateIsEmpty = False
                
                self._matrixA[cell[XINDEX]][cell[YINDEX]][i] += cell[STATEINDEX][i]
            else:
                # check, whether the old state of the given cell is empty or not
                if (self._matrixB[cell[XINDEX]][cell[YINDEX]][i] != 0):
                    oldStateIsEmpty = False
                
                self._matrixB[cell[XINDEX]][cell[YINDEX]][i] += cell[STATEINDEX][i]
        
        # if new state is not empty and old state is empty, add to next stack
        if ((not newStateIsEmpty) & oldStateIsEmpty):
            self.__addToNextStack(cell[XINDEX], cell[YINDEX])
    
    
    # private internal functions
    
    
    ## Add the given index to the next stack.
    #
    # @param x abscissa index of the given cell
    # @param y ordinate index of the given cell
    def __addToNextStack(self, x, y):
        if (self.__useP): # read from stackP and write to stackQ
            self.__stackQ.append([x, y])
        else: # read from stackQ and write to stackP
            self.__stackP.append([x, y])
    
    ## Fill the stack. This must be done after initialization of the data-structure. 
    def __fillStack(self):
        stack = []
        for i in range(self._numx):
            for j in range(self._numy):
                if (self._getUseA() # filled CA is in matrixB
                    & (self._matrixB[i][j][0] != 0) | (self._matrixB[i][j][1] != 0)):
                    # found non-zero element
                    stack.append([i, j])
                elif ((self._matrixA[i][j][0] != 0) | (self._matrixA[i][j][1] != 0)):
                    # found non-zero element
                    stack.append([i, j])
        
        # save stack
        if (self.__useP):
            self.__stackP = stack
        else:
            self.__stackQ = stack