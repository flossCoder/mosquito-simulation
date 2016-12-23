# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testTransformer.py
# Copyright (C) 2016 flossCoder
# 
# testTransformer.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testTransformer.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testTransformer defines the identity transformation on the coordinates.

from coordinateTransformer import CoordinateTransformer

## TestTransformer is written for testing purpose. It should NOT be used in "real" application. 
class TestTransformer(CoordinateTransformer):
    ## The init function must be overwritten. Otherwise one could not initialize an object.
    def __init__(self):
        pass
    
    
    # public functions
    
    
    ## transform the given external coordinates to internal coordinates
    #
    # @param a first coordinate
    # @param b second coordinate
    #
    # @return internal coordinates, which are the same as the external ones
    def calcInnerCoordinate(self, a, b):
        return [a, b]
    
    ## transform the given internal coordinates to external coordinates
    #
    # @param cellx abscissa index of the given cell
    # @param celly ordinate index of the given cell
    #
    # @return external coordinates, which are the same as the internal ones
    def calcOuterCoordinate(self, cellx, celly):
        return [cellx, celly]