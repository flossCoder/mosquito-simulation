# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# abstractInput.py
# Copyright (C) 2016 flossCoder
# 
# abstractInput.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# abstractInput.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package abstractInput defines the superclass for all input classes.

## AbstractInput defines an abstract class which is used to implement the data input.
class AbstractInput(object):
    ## default init function
    #
    # @param coordinateTransformer can transform the internal indexes to real coordinates (used
    # by GIS for example) and vice versa
    def __init__(self, coordinateTransformer):
        self._coordinateTransformer = coordinateTransformer
    
    
    # getter functions
    
    
    ## gather the data for the given cell
    #
    # @param day of simulation
    # @param cell index which is needed, format [x, y]
    #
    # @return a list with the values of the cell
    #
    # @exception NotImplementedError forces one to implement this function
    def getDataOfCell(self, day, cell):
        raise NotImplementedError("getDataOfCell has not yet been implemented")
    
    ## returns the initial state of the cellular automata
    #
    # @return an array containing abscissa, ordinate, mosquitos and larvae
    #
    # @exception NotImplementedError forces one to implement this function
    def getInitialState(self):
        raise NotImplementedError("getInitialState has not yet been implemented")