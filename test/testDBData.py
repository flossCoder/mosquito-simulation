# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# testDBData.py
# Copyright (C) 2016 flossCoder
# 
# testDBData.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# testDBData.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package testDBData for testing dbData.

import unittest

from constants import *
from dbData import DBData
from dbTransformer import DBTransformer
from helper import getComparator5x4, getZero, listsEqualTest
import psycopg2 as db
from setupTests import DBNAME, USERNAME, HOST, PASSWORD, TESTTABLENAME

## Test the DBData with a test database.
class TestDBData(unittest.TestCase):
    ## Prepare the test.
    def setUp(self):
        self.__dataArgs = {NAMEARGS:TESTTABLENAME,
                           DBNAMEARGS:DBNAME,
                           USERARGS:USERNAME,
                           HOSTARGS:HOST,
                           PASSWORDARGS:PASSWORD,
                           NEWTABLEARGS:True,
                           WIDTHARGS:5,
                           HEIGHTARGS:4,
                           UPPERLEFTXARGS:0.0005,
                           UPPERLEFTYARGS:0.0005,
                           SCALEXARGS:1,
                           SCALEYARGS:1,
                           SKEWXARGS:0,
                           SKEWYARGS:0,
                           SRIDARGS:SRIDUNKNOWN}
        self.__dbData = DBData(self.__dataArgs[NAMEARGS],
                               DBTransformer(),
                               self.__dataArgs[DBNAMEARGS],
                               self.__dataArgs[USERARGS],
                               self.__dataArgs[HOSTARGS],
                               self.__dataArgs[PASSWORDARGS],
                               self.__dataArgs[NEWTABLEARGS],
                               self.__dataArgs[WIDTHARGS],
                               self.__dataArgs[HEIGHTARGS],
                               self.__dataArgs[UPPERLEFTXARGS],
                               self.__dataArgs[UPPERLEFTYARGS],
                               self.__dataArgs[SCALEXARGS],
                               self.__dataArgs[SCALEYARGS],
                               self.__dataArgs[SKEWXARGS],
                               self.__dataArgs[SKEWYARGS],
                               self.__dataArgs[SRIDARGS])
        # the following data structure will be needed for the testing
        self.__ca = getComparator5x4()
    
    ## Finish the test.
    def tearDown(self):
        # connect to the db
        conn = db.connect("""dbname=%s user=%s host=%s password=%s""" % 
                          (self.__dataArgs[DBNAMEARGS],
                           self.__dataArgs[USERARGS],
                           self.__dataArgs[HOSTARGS],
                           self.__dataArgs[PASSWORDARGS]))
        # fetch the cursor
        cur = conn.cursor()
        # drop the table
        cur.execute("""DROP TABLE %s;""" % (self.__dataArgs[NAMEARGS]))
        # commit the changes
        conn.commit()
        # close the connection
        conn.close()
    
    ## Test the saveStep function.
    def testSaveStep(self):
        self.__dbData.saveStep(self.__ca, 0)
        equal = listsEqualTest(self.__ca,
                       self.__loadData())
        self.assertTrue(equal, "testSaveStep failed")
    
    ## Test the loadData function.
    def testLoadData(self):
        self.__dbData.saveStep(self.__ca, 0) # this function has been tested before
        #                                      => should work here too
        equal = listsEqualTest(self.__ca, self.__dbData.loadStep(0,
                                                         self.__dataArgs[WIDTHARGS],
                                                         self.__dataArgs[HEIGHTARGS]))
        self.assertTrue(equal, "testLoadData failed")
    
    ## Helping function to load a CA from the database independent from DBData for comparison.
    #
    # @param day to load, default day is 0
    def __loadData(self, day = 0):
        # connect to the db
        conn = db.connect("""dbname=%s user=%s host=%s password=%s""" % 
                          (self.__dataArgs[DBNAMEARGS],
                           self.__dataArgs[USERARGS],
                           self.__dataArgs[HOSTARGS],
                           self.__dataArgs[PASSWORDARGS]))
        # fetch the cursor
        cur = conn.cursor()
        # get the data
        step = getZero(self.__dataArgs[WIDTHARGS], self.__dataArgs[HEIGHTARGS])
        for i in range(self.__dataArgs[WIDTHARGS]):
            for j in range(self.__dataArgs[HEIGHTARGS]):
                cur.execute("""SELECT ST_Value(rast, 1, %i, %i) AS adults,
                ST_Value(rast, 2, %i, %i) AS larvae FROM %s
                WHERE %s.day = %i;""" % ((i + 1),
                                         (j + 1),
                                         (i + 1),
                                         (j + 1),
                                         self.__dataArgs[NAMEARGS],
                                         self.__dataArgs[NAMEARGS],
                                         day))
                answer = cur.fetchall()
                step[i][j] = [int(answer[0][0]), int(answer[0][1])]
        # close the connection
        conn.close()
        return step