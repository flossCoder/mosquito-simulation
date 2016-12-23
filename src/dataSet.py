# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# dataSet.py
# Copyright (C) 2016 flossCoder
# 
# simulationController.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# dataSet.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package dataSet defines the output set.

from constants import TYPEDB

## DataSet contains a list with outputs and is the output manager for the results of the
# simulation. Furthermore can saved data be loaded.
# WARNING for loading one should prefer a database using an index for better efficiency.
class DataSet:
    ## Initialize a new dataSet.
    def __init__(self):
        self.__dataSet = []
        self.__firstIsDB = False # first entry of the list is a database
    
    
    # public functions (interfaces for the environment)
    
    
    ## Add a new data object to the list. Check if first one is connector do DB. If not (and data
    # is a DB connector) insert data on first position. 
    #
    # @param data to add
    def addData(self, data):
        if (not(self.__firstIsDB) & (data.getType() == TYPEDB)):
            self.__dataSet.insert(0, data) # insert the database to position 0
            self.__firstIsDB = True
        else:
            self.__dataSet.append(data) # just append to the list
    
    ## Remove given data set.
    #
    # @param dataName name of the data set
    #
    # @exception list is empty
    def removeData(self, dataName):
        if (len(self.__dataSet) == 0):
            raise Exception("Data set is empty.")
        dbIndex = None # index of the last DB
        i = 0
        while (i < range(len(self.__dataSet))):
            if (self.__dataSet[i].getName() == dataName):
                self.__dataSet.pop(i)
                i = i - 1
                # remove i'th element
            elif (self.__dataSet[i].getType() == TYPEDB):
                dbIndex = i
        
        if ((self.__dataSet[0].getType == TYPEDB) & (self.__firstIsDB) & (dbIndex != None)):
            self.__dataSet.insert(0, self.__dataSet.pop(dbIndex)) # move DB to first position
    
    ## Save the given step to all registered elements.
    #
    # @param ca to save
    # @param day to save
    #
    # @exception list is empty
    def saveStep(self, ca, day):
        if (len(self.__dataSet) == 0):
            raise Exception("Data set is empty, you can't save something.")
        for elem in self.__dataSet:
            elem.saveStep(ca, day)
    
    ## Open a simulation step.
    #
    # @param day of simulation to open.
    #
    # @return the state of the CA at the given day.
    #
    # @exception list is empty
    def openStep(self, day):
        if (len(self.__dataSet) == 0):
            raise Exception("Data set is empty, you can't open a step.")
        return self.__dataSet[0].openStep(day)