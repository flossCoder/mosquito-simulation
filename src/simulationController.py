# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# simulationController.py
# Copyright (C) 2016 flossCoder
# 
# simulationController.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# simulationController.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package simulationController controls the whole tool and is the interface for the environment.

from combiCA import CombiCA
from constants import *
from dataSet import DataSet
from dbData import DBData
from dbTransformer import DBTransformer
from dispersionRule import DispersionRule
from habitatSimpleInput import HabitatSimpleInput
from simpleData import SimpleData
from simpleInput import SimpleInput
from testRule import TestRule
from testTransformer import TestTransformer

## The SimulationController controls the whole simulation containing initialization of IO and CA,
# the real simulation containing IO and the simulation steps. Furthermore defines the
# SimulationController the interface for the UI.
class SimulationController:
    ## Initialize the SimulationController.
    #
    # @param numx the number of cells on the abscissa
    # @param numy the number of cells on the ordinate
    # @param enableSaving allows to save; True: saving enabled (default), False: saving disabled
    def __init__(self, numx, numy, enableSaving = True):
        self.__input = None
        self.__ca = None
        self.__output = DataSet()
        self.__day = 0 # day after start of simulation (day = 0 is initial state!!!)
        self.__numx = numx # the number of cells on the abscissa
        self.__numy = numy # the number of cells on the ordinate
        self.__enableSaving = enableSaving # True: saving enabled, False: saving disabled
    
    
    # public initialize functions
    
    
    ## Do the initialization for benchmarking. Do NOT use this method otherwise.
    #
    # @param inputTransformerName the name of the transformer for the input
    # @param outputTransformerName the name of the transformer for the output
    # @param inputName the name of the input (e.g. simpleInput)
    # @param caName the name of the CA to use (e.g. CombiCA).
    # @param ruleName the rule for calculating the simulation-step (e.g. testRule, MALCAM).
    # @param dataName the name of the data to use (e.g. simpleData)
    # @param inputArgs is a dictionary containing additional arguments for the input
    # @param caArgs is a dictionary containing additional arguments for the CA
    # @param ruleArgs is a dictionary containing additional arguments for the used rule
    # @param dataArgs is a dictionary containing additional arguments for the used rule
    # @param methodToUse is an optional parameter to set the method to use from outside.
    # @param inputTransformerArgs is a dictionary containing additional arguments for the
    # coordinateTransformer for the input
    # @param outputTransformerArgs is a dictionary containing additional arguments for the
    # coordinateTransformer for the output
    def initBenchmark(self, inputTransformerName, inputName, caName, ruleName,
                      inputArgs, initCA, methodToUse, ruleArgs = None, caArgs = None):
        # set up the inputTransformer
        inputTransformer = self.initCoordinateTransformer(inputTransformerName, None)
        # initialize the input
        self.initInput(inputTransformer, inputName, inputArgs)
        # initialize the CA with the given initCA
        self.initCA(caName, ruleName, initCA, caArgs, ruleArgs, methodToUse)
    
    ## Do the initialization for testing purpose. Do NOT use this method otherwise.
    #
    # @param inputTransformerName the name of the transformer for the input
    # @param outputTransformerName the name of the transformer for the output
    # @param inputName the name of the input (e.g. simpleInput)
    # @param caName the name of the CA to use (e.g. CombiCA).
    # @param ruleName the rule for calculating the simulation-step (e.g. testRule, MALCAM).
    # @param dataName the name of the data to use (e.g. simpleData)
    # @param inputArgs is a dictionary containing additional arguments for the input
    # @param caArgs is a dictionary containing additional arguments for the CA
    # @param ruleArgs is a dictionary containing additional arguments for the used rule
    # @param dataArgs is a dictionary containing additional arguments for the used rule
    # @param methodToUse is an optional parameter to set the method to use from outside.
    # @param inputTransformerArgs is a dictionary containing additional arguments for the
    # coordinateTransformer for the input
    # @param outputTransformerArgs is a dictionary containing additional arguments for the
    # coordinateTransformer for the output
    def initTest(self, inputTransformerName, outputTransformerName, inputName, caName, ruleName,
                 dataName, inputArgs = None, caArgs = None, ruleArgs = None, dataArgs = None,
                 methodToUse = None, inputTransformerArgs = None, outputTransformerArgs = None):
        # set up the inputTransformer
        inputTransformer = self.initCoordinateTransformer(inputTransformerName, inputTransformerArgs)
        # set up the outputTransformer
        outputTransformer = self.initCoordinateTransformer(outputTransformerName, outputTransformerArgs)
        # initialize the input
        self.initInput(inputTransformer, inputName, inputArgs)
        # initialize the data
        self.initData(dataName, outputTransformer, dataArgs)
        # initialize the CA
        initCA = self.__input.getInitialState() # initial state of the CA
        self.initCA(caName, ruleName, initCA, caArgs, ruleArgs, methodToUse)
    
    ## Initialize coordinateTransformer (needed for input / output).
    #
    # @param coordinateTransformerName the name of the coordinateTransformer
    # (e.g. testTransformer)
    # @param coordinateTransformerArgs is a dictionary containing additional arguments for
    # the coordinateTransformer
    #
    # @return the coordinateTransformer object specified by coordinateTransformerName
    #
    # @exception invalid coordinateTransformerName
    def initCoordinateTransformer(self, coordinateTransformerName,
                                  coordinateTransformerArgs = None):
        if (coordinateTransformerName == TESTTRANSFORMER):
            return TestTransformer()
        elif (coordinateTransformerName == DBTRANSFORMER):
            return DBTransformer()
        else:
            raise Exception("coordinateTransformerName = %s is invalid" % 
                            coordinateTransformerName)
    
    ## Initialize Input.
    #
    # @return the initial state of the CA
    #
    # @param coordinateTransformer can transform the internal indexes to real coordinates (used
    # by GIS for example) and vice versa
    # @param inputName the name of the input (e.g. simpleInput)
    # @param inputArgs is a dictionary containing additional arguments for the input
    #
    # @exception invalid inputName
    def initInput(self, coordinateTransformer, inputName, inputArgs = None):
        if (inputName == SIMPLEINPUT):
            # for using SimpleInput inputArgs must contain CAINITNAMEARGS, DIRECTORYARGS,
            # THETAARGS, MARGS, RARGS, QARGS
            self.__input = SimpleInput(coordinateTransformer,
                                       inputArgs[CAINITNAMEARGS], # file name for loading the initial state
                                       inputArgs[DIRECTORYARGS], # storage directory for the files
                                       self.__numx, # number of cells in abscissa
                                       self.__numy, # number of cells in ordinate
                                       inputArgs[THETAARGS], # temperature in degree celsius
                                       inputArgs[MARGS], # mortality rate for the adults
                                       inputArgs[RARGS], # reproduction rate for the adults
                                       inputArgs[QARGS]) # quality of the hotbeds
        elif (inputName == HABITATSIMPLEINPUT):
            self.__input = HabitatSimpleInput(coordinateTransformer,
                                       inputArgs[CAINITNAMEARGS], # file name for loading the initial state
                                       inputArgs[DIRECTORYARGS], # storage directory for the files
                                       self.__numx, # number of cells in abscissa
                                       self.__numy, # number of cells in ordinate
                                       inputArgs[THETAARGS], # temperature in degree celsius
                                       inputArgs[MARGS], # mortality rate for the adults
                                       inputArgs[RARGS], # reproduction rate for the adults
                                       inputArgs[QNAMEARGS]) # file name with the quality of hotbeds
        else:
            raise Exception("inputName = %s is invalid" % (inputName))
    
    ## Initialize the data (used for output and loading of a saved CA state).
    #
    # @param dataName the name of the data to use (e.g. simpleData)
    # @param coordinateTransformer can transform the internal indexes to real coordinates (used
    # by GIS for example) and vice versa
    # @param dataArgs is a dictionary containing additional arguments for the used rule
    #
    # @exception the given dataName is invalid
    def initData(self, dataName, coordinateTransformer, dataArgs = None):
        if (dataName == SIMPLEDATA):
            # for using SimpleData dataArgs must contain NAMEARGS and DIRECTORYARGS
            self.__output.addData(SimpleData(dataArgs[NAMEARGS], # name of the data, will be used as a filename
                                             coordinateTransformer,
                                             dataArgs[DIRECTORYARGS])) # the directory where the file should be saved
        elif (dataName == DBDATA):
            # for using DBData dataArgs must contain NAMEARGS, DBNAMEARGS, USERARGS, HOSTARGS,
            # PASSWORDARGS, NEWTABLEARGS, WIDTHARGS, HEIGHTARGS, UPPERLEFTXARGS, UPPERLEFTYARGS,
            # SCALEXARGS, SCALEYARGS, SKEWXARGS, SKEWYARGS and SRIDARGS
            self.__output.addData(DBData(dataArgs[NAMEARGS], # name of the data, will be used as a table name
                                         coordinateTransformer,
                                         dataArgs[DBNAMEARGS], # name of the database
                                         dataArgs[USERARGS], # name of the user, make sure user has access to the database!
                                         dataArgs[HOSTARGS], # host name (if the database is local, just 'localhost')
                                         dataArgs[PASSWORDARGS], # password of the database user
                                         dataArgs[NEWTABLEARGS], # newTable True: create a new table with the given name; False: don't create a new table
                                         dataArgs[WIDTHARGS], # number of cells on the abscissa
                                         dataArgs[HEIGHTARGS], # number of cells on the ordinate
                                         dataArgs[UPPERLEFTXARGS], # x value of the upper left cell
                                         dataArgs[UPPERLEFTYARGS], # y value of the upper left cell
                                         dataArgs[SCALEXARGS], # pixel size on the abscissa
                                         dataArgs[SCALEYARGS], # pixel size on the ordinate
                                         dataArgs[SKEWXARGS], # rotation of the cells on the abscissa
                                         dataArgs[SKEWYARGS], # rotation of the cells on the ordinate
                                         dataArgs[SRIDARGS])) # srid (spatial reference id) defines the coordinate system
        else:
            raise Exception("dataName = %s is invalid" % dataName)
    
    ## Initialize the CA.
    #
    # @param caName the name of the CA to use (e.g. CombiCA).
    # @param ruleName the rule for calculating the simulation-step (e.g. testRule, MALCAM).
    # @param initCA the initial CA
    # @param caArgs is a dictionary containing additional arguments for the CA
    # @param ruleArgs is a dictionary containing additional arguments for the used rule
    # @param methodToUse is an optional parameter to set the method to use from outside.
    #
    # @exception invalid ruleName
    # @exception invalid caName
    def initCA(self, caName, ruleName, initCA,
               caArgs = None, ruleArgs = None, methodToUse = None):
        rule = None
        if (ruleName == TESTRULE):
            # for using TestRule ruleArgs must contain "DISPERSIONARGS" True or False
            rule = TestRule(ruleArgs[DISPERSIONARGS]) # dispersion on (True) or off (False)
        elif (ruleName == DISPERSIONRULE):
            # for using DispersionRule ruleArgs must contain "AREAARGS" and "MOVINGFACTORARGS"
            rule = DispersionRule(self.__numx, self.__numy,
                                  ruleArgs[AREAARGS], ruleArgs[MOVINGFACTORARGS])
        else:
            raise Exception("ruleName = %s is invalid" % ruleName)
        
        if (caName == COMBICA):
            self.__ca = CombiCA(self, rule, self.__numx, self.__numy, initCA, methodToUse)
        else:
            raise Exception("caName = %s is invalid" % caName)
    
    
    # public functions (interfaces for the environment)
    
    
    ## doSimulation controls the simulation and is responsible for saving the data
    # The initial- (day 0) and the final step will always be saved.
    #
    # @param numSteps the number of steps for the simulation
    # @param saveStep each saveStep's day the state of the CA will be saved
    #
    # @exception Invalid numSteps, if numSteps < 1.
    # @exception Invalid saveStep, if saveStep > numSteps
    def doSimulation(self, numSteps, saveStep = None):
        lastSavedStep = 0 # The last step which was saved.
        # save initial state
        if self.__enableSaving:
            self.__saveData()
            lastSavedStep = self.__day
        self.__day += 1
        if (saveStep != None):
            if (numSteps < 1):
                raise Exception("The given number of Steps = %i is invalid, because a simulation with less then one day is senseless." % numSteps)
            if (saveStep > numSteps):
                raise Exception("The saving interval = %i can't be bigger than the number of steps = %i" % (saveStep, numSteps))
        
        for day in range(numSteps):
            self.__ca.doStep() # do the whole calculation
            if (self.__enableSaving & (saveStep != None)): # want to save the data?
                if ((day % saveStep) == saveStep - 1):
                    self.__saveData()
                    lastSavedStep = self.__day
            self.__day += 1
        if (lastSavedStep != numSteps) & self.__enableSaving:
            # Has the last Step been saved? If not, save it.
            self.__day -= 1
            self.__saveData()
            self.__day += 1
    
    
    ## Load data and set the CA to the right state
    #
    # @param day of simulation.
    def loadData(self, day):
        self.__ca.setCA(self.__output.loadData(day))
        self.__day = day
    
    
    # getter functions
    
    
    ## getRuleName returns the name of the used rule
    #
    # @return the name of the used rule
    def getRuleName(self):
        return self.__ca.getRuleName()
    
    ## getRuleCite returns the citation of the used rule
    #
    # @return the citation of the used rule
    def getRuleCite(self):
        return self.__ca.getRuleCite()
    
    ## get the data for the simulation of the given cell for the given day
    #
    # @param cell index which is needed, format [x, y]
    #
    # @return required data
    def getDataOfCell(self, cell):
        return self.__input.getDataOfCell(self.__day, cell)
    
    ## getCA returns the current CA as a python-list
    #
    # @return the matrix of the CA
    def getCA(self):
        return self.__ca.getCA()
    
    
    # setter functions
    
    
    ## set the input
    #
    # @param input a new inheritance of the input class
    def setInput(self, input):
        self.__input = input
    
    
    # private internal functions
    
    
    ## Save the current state of the CA.
    def __saveData(self):
        self.__output.saveStep(self.__ca.getCA(), self.__day)