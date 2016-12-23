# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-
#
# zeroCA.py
# Copyright (C) 2016 flossCoder
#
# zeroCA.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# zeroCA.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package zeroCA defines a function to set up an empty numx * numy CA

## Setup an empty CA.
#
# @param length number of parameter in the CA
# @param numx the number of cells on the abscissa
# @param numy the number of cells on the ordinate
#
# @return an empty numx * numy CA
def zeroCA(length, numx, numy):
    return [[[0 for h in range(length)] for i in range(numy)] for j in range(numx)]