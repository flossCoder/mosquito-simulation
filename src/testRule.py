# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testRule.py
# Copyright (C) 2016 flossCoder
# 
# testRule.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testRule.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testRule defines a CA rule for testing purpose and should NOT be used otherwise.

from abstractRule import AbstractRule
from constants import XINDEX, YINDEX, STATEINDEX

## TestRule is a rule defined to test the behavior of the CA, especially of "touching" the
# correct cells in the different algorithms.
class TestRule(AbstractRule):
    ## Set up the TestRule.
    #
    # @param dispersion on (True) or off (False)
    def __init__(self, dispersion):
        super().__init__("TestRule: Do NOT use TestRule outside of tests.", "No citation: Do NOT use TestRule outside of tests.")
        self.__dispersion = dispersion
    
    
    # public functions (interfaces for the environment)
    
    
    ## This function implements the calculation of the values.
    #
    # @param cell to calculate, format [x, y, [adults, larvae], [theta, m, r, q]]
    # @param neighourhood of the cell to calculate, format
    #                     [[x0, y0, [adults, larvae], [theta0, m0, r0, q0]], ...]
    #
    # @return new state of the given cells, format [[x, y, [adults, larvae]], ...]
    def calculateValues(self, cell, neighborhood):
        if self.__dispersion: # dispersion
            result = [[cell[XINDEX], cell[YINDEX], cell[STATEINDEX]]] # current cell
            for elem in neighborhood:
                result.append([elem[XINDEX],
                               elem[YINDEX],
                               [1, 1]])
            return result
        else: # no dispersion
            return [[cell[XINDEX], cell[YINDEX],
                     [(cell[STATEINDEX][0] + 1000), (cell[STATEINDEX][1] + 100)]]]
    
    
    # setter functions
    
    
    ## This function sets the dispersion flag.
    #
    # @param dispersion True: with dispersion, False: no dispersion
    def setDispersion(self, dispersion):
        self.__dispersion = dispersion