# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# easyCA.py
# Copyright (C) 2016 flossCoder
# 
# easyCA.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# easyCA.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package easyCA implements the easy method.

from abstractMatrix import AbstractMatrix

## EasyCA implements the easy method, which is good for dense CA.
class EasyCA(AbstractMatrix):
    ## initialize the data structure
    #
    # @param combiCA needed for communication
    # @param numx the number of cells on the abscissa
    # @param numy the number of cells on the ordinate
    # @param initCA the initial CA
    def __init__(self, combiCA, numx, numy, initCA):
        super().__init__(combiCA, numx, numy, initCA)
    
    
    # protected functions (can be used from derivative classes)
    
    
    ## doStep performs one simulation step
    def _performCalculation(self):
        # go through all cells, start with the one left bottom
        for i in range(self._numx):
            for j in range(self._numy):
                self._simulateCurrentCell([i, j])