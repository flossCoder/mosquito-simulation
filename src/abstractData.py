# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# dataSet.py
# Copyright (C) 2016 flossCoder
# 
# abstractData.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# abstractData.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package abstractData defines the superclass for the data classes.

## AbstractData defines the interface for data classes.
class AbstractData(object):
    ## Init function for setting type and name by subclasses.
    #
    # @param type (e. g. database, CSV, ...)
    # @param name of the data
    # @param coordinateTransformer can transform the internal indexes to real coordinates (used
    # by GIS for example) and vice versa
    def __init__(self, type, name, coordinateTransformer):
        self._type = type
        self._name = name
        self._coordinateTransformer = coordinateTransformer
    
    
    # public functions (interfaces for the environment)
    
    
    ## Save the given step to all registered elements.
    #
    # @param ca to save
    # @param day to save
    #
    # @exception NotImplementedError forces one to implement this function
    def saveStep(self, ca, day):
        raise NotImplementedError("saveStep has not yet been implemented")
    
    ## Open a simulation step.
    #
    # @param day of simulation to load
    # @param numx number of cells on abscissa
    # @param numy number of cells on ordinate
    #
    # @return the state of the CA on the given day
    #
    # @exception NotImplementedError forces one to implement this function
    def loadStep(self, day, numx, numy):
        raise NotImplementedError("loadStep has not yet been implemented")
    
    
    # getter functions
    
    
    ## Getter for self._type
    #
    # @return type
    def getType(self):
        return self._type
    
    ## Getter for self._name
    #
    # @return name
    def getName(self):
        return self._name
    
    
    # setter functions
    
    
    ## Setter for self.__name
    #
    # @param name the new name
    def setName(self, name):
        self.__name = name