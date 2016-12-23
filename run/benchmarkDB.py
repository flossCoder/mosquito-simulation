# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# benchmarkDB.py
# Copyright (C) 2016 flossCoder
# 
# benchmarkDB.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# benchmarkDB.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package benchmarkDB measures the saving and loading from CA's into the DB and in comparison
# into a CSV file depending on the day.

import csv
from os import remove
from time import clock

from dbData import DBData
from dbTransformer import DBTransformer
import psycopg2 as db
from setupRun import DIRECTORY
from simpleData import SimpleData
from testTransformer import TestTransformer


# basic variable set-up
directoryOut = "%s/benchmarkDB" % DIRECTORY # set directory for loading files

dbTransformer = DBTransformer()
testTransformer = TestTransformer()

dbname = "test"
user = "postgres"
host = "localhost"
password = "bodhi"
name = "testraster"

width = 20
height = 20
maxDay = 100

file = "%s/%s_%i.csv" % (directoryOut, "dbTest", (width * height))

# delete CSV file with results if required
try:
    remove(file)
except:
    pass

# measure the load- and save times of a CA for different days using CSV and DB
with open(file, 'a', newline = '') as csvfile:
    data = csv.writer(csvfile, delimiter = ",")
    initCA = [[[1 for h in range(2)] for i in range(height)] for j in range(width)]
    # initialize SimpleData
    simpleData = SimpleData("test", testTransformer, directoryOut)
    # initialize DBData
    dbData = DBData(name,
                    dbTransformer,
                    dbname,
                    user,
                    host,
                    password,
                    True,
                    width,
                    height,
                    0.0005,
                    0.0005,
                    1,
                    1,
                    0,
                    0)
    print("start measure time for saving in DB and CSV")
    for day in range(0, maxDay + 1):
        # save CSV
        timeSaveCSV = clock()
        simpleData.saveStep(initCA, day)
        timeSaveCSV = clock() - timeSaveCSV
        
        # load CSV
        timeLoadCSV = clock()
        simpleData.loadStep(day, width, height)
        timeLoadCSV = clock() - timeLoadCSV
        
        # save DB
        timeSaveDB = clock()
        dbData.saveStep(initCA, day)
        timeSaveDB = clock() - timeSaveDB
        
        # load DB
        timeLoadDB = clock()
        dbData.loadStep(day, width, height)
        timeLoadDB = clock() - timeLoadDB
        
        # save measured values
        data.writerow([day, timeSaveCSV, timeLoadCSV, timeSaveDB, timeLoadDB])
        print("day: %i save CSV: %f load CSV: %f save DB: %f load DB: %f" % (day,
                                                                              timeSaveCSV,
                                                                              timeLoadCSV,
                                                                              timeSaveDB,
                                                                              timeLoadDB))
        
    # clean up
    # remove test.csv
    remove("%s/test.csv" % directoryOut)
    # drop table
    # connect to db
    conn = db.connect("dbname=%s user=%s host=%s password=%s" % (dbname, user, host, password))
    # fetch the cursor
    cur = conn.cursor()
    cur.execute("""DROP TABLE %s""" % (name))
    # commit changes
    conn.commit()
    # close the db connection
    conn.close()

print("done")