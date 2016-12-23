# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# abstractCA.py
# Copyright (C) 2016 flossCoder
# 
# abstractCA.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# abstractCA.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package abstractCA defines the superclass for the implementation of the cellular automaton.

## AbstractCA defines an abstract class which is used to implement the cellular automaton.
class AbstractCA(object):
    ## init function
    #
    # @param controller needed for receiving simulation data
    # @param rule for calculating the simulation step
    def __init__(self, controller, rule):
        self._controller = controller
        self._rule = rule
        self._rule.setCA(self)
    
    
    # public functions (interfaces for the environment)
    
    
    ## This function implements the calculation of the values.
    #
    # @param cell to calculate, format [x, y, adults, larvae, theta, m, r, q]
    # @param neighourhood of the cell to calculate, format
    #                     [[x0, y0, adults, larvae, theta0, m0, r0, q0], ...]
    #
    # @return new state of the given cells, format [[x, y, adults, larvae], ...]
    def calculateValues(self, cell, neighbourhood):
        return self._rule.calculateValues(cell, neighbourhood)
    
    ## doStep performs one simulation step
    #
    # @exception NotImplementedError forces one to implement this function
    def doStep(self):
        raise NotImplementedError("doStep has not yet been implemented")
    
    
    # getter functions 
    
    
    ## getRuleName returns the name of the used rule
    #
    # @return the name of the used rule
    def getRuleName(self):
        return self._rule.getName()
    
    ## getRuleCite returns the citation of the used rule
    #
    # @return the citation of the used rule
    def getRuleCite(self):
        return self._rule.getCite()
    
    ## get the data for the simulation of the given cell
    #
    # @param cell index which is needed, format [x, y]
    #
    # @return required data
    def getDataOfCell(self, cell):
        return self._controller.getDataOfCell(cell)
    
    ## getCA returns the current CA as a Python-list
    #
    # @return the CA
    #
    # @exception NotImplementedError forces one to implement this function
    def getCA(self):
        raise NotImplementedError("getCA has not yet been implemented")
    
    ## get the data for the simulation of the given cells
    #
    # @param cells indexes are needed
    #
    # @return required data plus the CA state of the previous time step
    #
    # @exception NotImplementedError forces one to implement this function
    def getDataOfCells(self, cells):
        raise NotImplementedError("getDataOfCells has not yet been implemented")
    
    
    # setter functions
    
    
    ## setCA is needed for initialization and loading a saved state 
    #
    # @param ca to use
    #
    # @exception NotImplementedError forces one to implement this function
    def setCA(self, ca):
        raise NotImplementedError("setCA has not yet been implemented")