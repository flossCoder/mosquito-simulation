# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# combiCA.py
# Copyright (C) 2016 flossCoder
# 
# combiCA.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# combiCA.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package combiCA contains the combined method.

from abstractCA import AbstractCA
from constants import EASYCA, STACKCA, XINDEX
from easyCA import EasyCA
from stackCA import StackCA

## CombiCA implements the combined method.
class CombiCA(AbstractCA):
    ## Initialize combiCA.
    #
    # @param controller needed for receiving simulation data
    #                   controller will be passed to the super class AbstractCA
    # @param rule for calculating the simulation step
    # @param numx the number of cells on the abscissa
    # @param numy the number of cells on the ordinate
    # @param initCA the initial CA
    # @param methodToUse is an optional parameter to set the method to use from outside.
    def __init__(self, controller, rule, numx, numy, initCA, methodToUse = None):
        # call the super init function of the super class AbstractCA
        super().__init__(controller, rule)
        
        self.__numx = numx # number of cells on abscissa
        self.__numy = numy # number of cells on Ordinate
        self.__method = None # which calculation method is used in this program
        self.__ca = None
        self.__recalculateMethodToUse = True # needed to force the usage of one method
        self.__stepsAfterMethodCheck = 0 # how many steps have been done until the last method
                                        # check
        self.__methodIntervall = 10 # interval for checking the method to use
        self.__threshold = 0.7963
        
        # calculate the method to use
        self.__decideMethod(initCA, methodToUse)
    
    
    # public functions (interfaces for the environment)
    
    
    ## doStep performs one simulation step
    def doStep(self):
        self.__ca.doStep()
        if (self.__recalculateMethodToUse):
            if (self.__stepsAfterMethodCheck < self.__methodIntervall):
                # decide, if the method to use has to be changed
                self.__decideMethod()
                self.__stepsAfterMethodCheck = 0
            else:
                # increment __stepsAfterMethodCheck
                self.__stepsAfterMethodCheck += 1
    
    
    # getter functions
    
    
    ## getCA returns the current CA as a python-list
    #
    # @return the CA
    def getCA(self):
        return self.__ca.getCA()
    
    ## get the data for the simulation of the given cells
    #
    # @param cells indexes are needed
    #
    # @return required data plus the CA state of the previous time step
    def getDataOfCells(self, cells):
        return self.__ca._getDataOfCells(cells)
    
    
    # setter functions
    
    
    ## setCA is needed for loading a saved state.
    #
    # @param CA to use
    # @param method used for simulation
    def setCA(self, ca, method = None):
        self.__decideMethod(ca, method)
    
    
    # private internal functions
    
    
    ## setOperation sets the algorithm which should be used for the simulation
    #
    # @param method used for simulation
    # @param initCA is used to decide the algorithm to use (if initCA = None, use the one of the
    # current state)
    #
    # @exception param method is invalid
    def __setMethod(self, method, initCA = None):
        if (self.__method == method):
            return # do nothing, the given method is currently set
        elif (self.__method == None): # set method the first time
            if (method == EASYCA):
                self.__ca = EasyCA(self, self.__numx, self.__numy, initCA)
                self.__method = EASYCA
                return
            elif (method == STACKCA):
                self.__ca = StackCA(self, self.__numx, self.__numy, initCA)
                self.__method = STACKCA
                return
            else:
                raise Exception("%s is no valid parameter" % (method))
        elif (method == EASYCA):
            self.__ca = EasyCA(self, self.__numx, self.__numy, self.__ca.getCA())
        elif (method == STACKCA):
            self.__ca = StackCA(self, self.__numx, self.__numy, self.__ca.getCA())
        else:
            raise Exception("method = %s contains invalid data" % (method))
        self.__method = method # set the name of the method
    
    ## decide with heuristics, which operation is used
    #
    # @param initCA is used to decide the algorithm to use (if initCA = None, use the one of the
    # current state)
    # @param methodToUse is an optional parameter to set the method to use from outside.
    # If methodToUse = None find the methodToUse with the heuristics.
    def __decideMethod(self, initCA = None, methodToUse = None):
        if (methodToUse != None):
            # if the initially given method is not None (e. g. the user forces the program to use
            # a certain method, this one is not changed during the simulation.
            self.__recalculateMethodToUse = False
        if (methodToUse == None):
            # find out the method to use via the heuristics
            if (initCA != None):
                # Initialize with given CA
                self.__setMethod(self.__heuristics(initCA), initCA) # set the method
            else:
                # Initialize with own CA
                self.__setMethod(self.__heuristics(), self.getCA())
        else:
            # use the given methodToUse 
            if (initCA != None):
                # Initialize with given CA
                self.__setMethod(methodToUse, initCA) # set the method
            else:
                # Initialize with own CA
                self.__setMethod(methodToUse, self.getCA())
        
    ## Implement the heuristics for using the right method.
    #
    # @param initCA is used to decide the algorithm to use (if initCA = None, use the one of the
    # current state)
    #
    # @return method to use for the simulation
    def __heuristics(self, initCA = None):
        if (initCA != None):
            if (self.__calcFillingDegree(initCA) < self.__threshold):
                return STACKCA
            else:
                return EASYCA
        elif (self.__computeFillingDegree() < self.__threshold):
            return STACKCA
        else:
            return EASYCA
    
    ## This function calculates the filling degree depending on the used method. For StackCA the
    # size of the stack can be used. For EasyCA the filling degree has to calculated new.
    #
    # @return the current filling degree
    def __computeFillingDegree(self):
        if (self.__method == STACKCA):
            return (self.__ca.getSizeOfStack() / (self.__numx * self.__numy))
        else:
            return (self.__calcFillingDegree(self.__ca.getCA()))
    
    ## Calculate the filling degree of the given CA.
    #
    # @param CA to calculate the filling degree.
    #
    # @return the filling degree
    def __calcFillingDegree(self, CA):
        numFilledCells = 0
        for elem1 in CA:
            for elem2 in elem1:
                # check state of cell on emptiness
                foundFilledCell = False
                for elem3 in elem2:
                    if (elem3 != 0):
                        foundFilledCell = True
                if (foundFilledCell): # is the cell not empty
                    numFilledCells += 1 # cell is not empty
        # divide number of filled cells through CA size
        return (numFilledCells / (len(CA) * len(CA[XINDEX])))