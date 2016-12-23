# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# coordinateTransformer.py
# Copyright (C) 2016 flossCoder
# 
# coordinateTransformer.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# coordinateTransformer.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package coordinateTransformer defines the interface for implementing a transformation between
# internal and external coordinates.

## CoordinateTransformer defines the interface which is used to implement the transformation from
# internal coordinates to real coordinates and vice versa.
class CoordinateTransformer(object):
    ## default init function
    #
    # @exception Exception keeping off initializing an CoordinateTransformer object
    def __init__(self):
        raise Exception("CoordinateTransformer is an interface")
    
    
    # public functions
    
    
    ## transform the given external coordinates to internal coordinates
    #
    # @param a first coordinate
    # @param b second coordinate
    #
    # @return internal coordinates
    #
    # @exception NotImplementedError forces one to implement this function
    def calcInnerCoordinate(self, a, b):
        raise NotImplementedError("getDataOfCell has not yet been implemented")
    
    ## transform the given internal coordinates to external coordinates
    #
    # @param cellx on abscissa
    # @param celly on ordinate
    #
    # @return external coordinates
    #
    # @exception NotImplementedError forces one to implement this function
    def calcOuterCoordinate(self, cellx, celly):
        raise NotImplementedError("getDataOfCell has not yet been implemented")