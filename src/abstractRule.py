# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# abstractRule.py
# Copyright (C) 2016 flossCoder
# 
# abstractRule.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# abstractRule.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package abstractRule defines the superclass for rules.

## Define the superclass for rules.
class AbstractRule(object):
    ## Initialize the object with name and citation.
    # This function should be called by subclasses.
    #
    # @param name of the rule
    # @param cite of the rule
    def __init__(self, name, cite):
        self._name = name
        self._cite = cite
        self._ca = None
    
    
    # public functions (interfaces for the environment)
    
    
    ## This function implements the calculation of the values.
    #
    # @param cell to calculate, format [x, y, adults, larvae, theta, m, r, q]
    # @param neighourhood of the cell to calculate, format
    #                     [[x0, y0, adults, larvae, theta0, m0, r0, q0], ...]
    #
    # @exception NotImplementedError forces one to implement this function
    def calculateValues(self, cell, neighbourhood):
        raise NotImplementedError("calculateValues has not yet been implemented")
    
    
    # getter functions
    
    
    ## get the name of the used rule
    #
    # @return name of the used rule
    #
    # @exception the name has not been set by the implementing class of AbstractRule.
    def getName(self):
        try:
            return self._name
        except:
            raise Exception("The name of the rule must be set by subclasses of AbstractRule.")
    
    ## get the citation of the used rule
    #
    # @return cite of the used rule
    #
    # @exception the cite has not been set by the implementing class of AbstractRule.
    def getCite(self):
        try:
            return self._cite
        except:
            raise Exception("The cite of the rule must be set by subclasses of AbstractRule.")
    
    ## get the data for the simulation of the given cells
    #
    # @param cells indexes are needed
    #
    # @return required data plus the CA state of the previous time step
    def getDataOfCells(self, cells):
        self._ca.getDataOfCells(cells)
    
    # setter functions
    
    
    ## set the ca.
    #
    # @param ca given
    def setCA(self, ca):
        self._ca = ca