# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# dispersionRule.py
# Copyright (C) 2016 flossCoder
# 
# dispersionRule.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# dispersionRule.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package dispersionRule defines a CA rule for proving that this system can simulate mosquito
# transportation over several cells using a random technique.
# This rule has been designed from a theoretical point of view.
# It has not been proven, if this rule defines a realistic description of the spreading
# of mosquitos.

from math import ceil
from random import random
from abstractRule import AbstractRule
from constants import XINDEX, YINDEX, STATEINDEX, CELLDATAINDEX

## Define a rule to calculate a transportation of mosquitos over a longer distance.
class DispersionRule(AbstractRule):
    ## Set up the DispersionRule.
    #
    # @param numx the number of cells on the abscissa
    # @param numy the number of cells on the ordinate
    # @param area of a cell in square meters
    # @param movingFactor probability for the moving adults to move over a long distance in [0, 1]
    def __init__(self, numx, numy, area, movingFactor):
        super().__init__("DispersionRule", "No citation: This rule is unpublished.")
        self._numx = numx
        self._numy = numy
        self._adultsMax = area * 1000 # assume, that 1000 adults live on one square meter
        self._movingFactor = movingFactor
    
    
    # public functions (interfaces for the environment)
    
    
    ## This function implements the calculation of the values.
    #
    # @param cell to calculate, format [x, y, [adults, larvae], [theta, m, r, q]]
    # @param neighourhood of the cell to calculate, format
    #                     [[x0, y0, [adults, larvae], [theta0, m0, r0, q0]], ...]
    #
    # @return new state of the given cells, format [[x, y, [adults, larvae]], ...]
    def calculateValues(self, cell, neighborhood):
        adults = int(cell[STATEINDEX][0])
        larvae = int(cell[STATEINDEX][1])
        theta = float(cell[CELLDATAINDEX][0])
        m = float(cell[CELLDATAINDEX][1])
        r = float(cell[CELLDATAINDEX][2])
        q = float(cell[CELLDATAINDEX][3])
        # security checks
        # is the mortality rate in [0, 1]:
        if ((m < 0) | (m > 1)):
            raise Exception("Invalid mortality rate: %f" % (m))
        # is the habitat quality in [0, 1]:
        if ((q < 0) | (q > 1)):
            raise Exception("Invalid habitat quality: %f" % (q))
        # calculate the new state
        d = self._calculateDevelopmentRate(theta)
        adultsMove = self._calculateAdultsMove(adults, d)
        stateNew = [[cell[XINDEX], cell[YINDEX],
                    [self._calculateAdults(adults, larvae, r, d, m, adultsMove, q),
                     self._calculateLarvae(adults, larvae, r, d)]]]
        stateNew.extend(self._calculateDispersion(neighborhood,
                                                  adultsMove,
                                                  cell[XINDEX],
                                                  cell[YINDEX]))
        return stateNew
    
    
    # protected functions (can be used from derivative classes)
    
    
    ## Calculate the number of larvae of the current cell.
    #
    # @param adults the number of adults of the current cell
    # @param larvae the number of larvae of the current cell
    # @param r the reproduction rate of the mosquitos
    # @param d the development rate of the larvae
    #
    # @return the number of larvae of the current cell
    def _calculateLarvae(self, adults, larvae, r, d):
        result = int(larvae + self._calculateReproducedLarvae(adults, r)
                            - self._calculateGrownLarvae(larvae, d))
        # check if result is smaller 0
        if (result < 0):
            return 0
        else:
            return result
    
    ## Calculate the number of adults of the current cell.
    #
    # @param adults the number of adults of the current cell
    # @param larvae the number of larvae of the current cell
    # @param r the reproduction rate of the mosquitos
    # @param d the development rate of the larvae
    # @param m the mortality rate
    # @param adultsMove the number of adults leaving the current cell
    # @param q the quality of the hotbeds
    #
    # @return the number of adults of the current cell
    def _calculateAdults(self, adults, larvae, r, d, m, adultsMove, q):
        res = (adults + (self._calculateGrownLarvae(larvae, d)
                    - self._calculateDiedAdults(adults, m)
                    - self._calculateAdultsMove(adults, d))
                    * self._calculateAdultsLimiter(adults, q))
        if (res > self._adultsMax * q):
            res = self._adultsMax * q
        result = int(res)
        # check if result is smaller 0
        if (result < 0):
            return 0
        else:
            return result
    
    ## Calculate the dispersion based partly on spreading adults uniformly distributed and partly
    # based on a technique influenced by Monte Carlo simulations.
    #
    # @param neighourhood of the cell to calculate, format
    #                     [[x0, y0, [adults, larvae], [theta0, m0, r0, q0]], ...]
    # @param adultsMove the number of adults leaving the current cell
    # @param cellx coordinate on the abscissa
    # @param celly coordinate on the ordinate
    #
    # @return the new dispersion
    def _calculateDispersion(self, neighborhood, adultsMove, cellx, celly):
        # calculate the number of adults that should move more then in distance of radius 1
        moveLongDistance = 0
        result = []
        guessedCell = self._guessCell()
        if (random() < self._movingFactor):
            result.append([guessedCell[XINDEX], guessedCell[YINDEX], [1, 0]])
            moveLongDistance = int(adultsMove * random())
        
        # spread rest of the moving adults on the neighborhood
        for neighborCell in neighborhood:
            # for each neighbor cell calculate the new state and append the result to sateNew
            adults = int(ceil((adultsMove - moveLongDistance) / len(neighborhood)))
            if (adults < 0):
                adults = 0
            result.append([neighborCell[XINDEX], # abscissa coordinate
                           neighborCell[YINDEX], # ordinate coordinate
                           [adults, 0]]) # moving adults
        
        return result
    
    ## Guess a new cell to place the mosquito.
    #
    # @return the cell index where to place the mosquito
    def _guessCell(self):        
        # guess cell
        return [int(self._numx * random()), int(self._numy * random())]
    
    ## Calculate the development rate of the larvae.
    #
    # @param theta the average daily temperature
    #
    # @return the development rate of the larvae
    def _calculateDevelopmentRate(self, theta):
        if ((theta <= 10) | (theta >= 40)):
            return 0.0
        elif (theta < 25):
            return (2.0 / 300.0 * theta - 2.0 / 30.0)
        else:
            return (-2.0 / 300.0 * theta + 8.0 / 30.0)
    
    ## Calculate the number of reproduced larvae.
    #
    # @param adults the number of adults of the current cell
    # @param r the reproduction rate of the mosquitos
    #
    # @return the number of reproduced larvae
    def _calculateReproducedLarvae(self, adults, r):
        return int(adults * r)
    
    ## Calculate the number of larvae which became adults.
    #
    # @param larvae the number of larvae of the current cell
    # @param d the development rate of the larvae
    #
    # @return the number of grown larvae
    def _calculateGrownLarvae(self, larvae, d):
        return int(larvae * d)
    
    ## Calculate the number of adults which died.
    #
    # @param adults the number of adults of the current cell
    # @param m the mortality rate
    #
    # @return the number of adults which died
    def _calculateDiedAdults(self, adults, m):
        return int(adults * m)
    
    ## Calculate the number of adults which leave the current cell.
    #
    # @param adults the number of adults of the current cell
    # @param d the development rate of the larvae (which will be taken as a rate for mosquitos
    #        leaving the current cell.
    #
    # @return the number of adults leaving the current cell
    def _calculateAdultsMove(self, adults, d):
        return int(adults * d)
    
    ## Calculate the limiting factor for the adults of the current cell.
    #
    # @param adults the number of adults of the current cell
    # @param q the quality of the hotbeds
    #
    # @return the limiting factor of the adults of the current cell
    def _calculateAdultsLimiter(self, adults, q):
        return (1.0 - adults / (self._adultsMax * q))