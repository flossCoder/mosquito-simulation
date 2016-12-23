# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# dbtest.py
# Copyright (C) 2016 flossCoder
# 
# dbtest.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# dbtest.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

# This script helps to save data from the database to CSV and remove the database.

import csv
from os import remove

import psycopg2 as db
from setupRun import DIRECTORY, DBNAME, USERNAME, HOST, PASSWORD, TESTTABLENAME


## Get data from DB and save them to CSV file.
#
# @param dbname name of the database
# @param user name of the user, make ensure user has access to the database!
# @param host name (if the database is local, just 'localhost')
# @param password of the database user
# @param name of the table (and CSV file)
# @param dir to save the CSV
# @param numx the number of cells on the abscissa
# @param numy the number of cells on the ordinate
# @param daymax last saved day
def save(dbname, user, host, password, directory, name, numx, numy, daymax):
    # connect to DB
    conn = db.connect("dbname=%s user=%s host=%s password=%s" % (dbname, user, host, password))
    # fetch the cursor
    cur = conn.cursor()
    # get the data and save them to CSV
    with open("%s/%s.csv" % (directory, name), 'a', newline = '') as csvfile:
        data = csv.writer(csvfile, delimiter = ",")
        for day in range(daymax + 1):
            for i in range(numx):
                for j in range(numy):
                    cur.execute("""SELECT ST_Value(rast, 1, %i, %i) AS adults,
                    ST_Value(rast, 2, %i, %i) AS larvae FROM %s
                    WHERE %s.day = %i;""" % ((i + 1), (j + 1), (i + 1), (j + 1), name, name, day))
                    answer = cur.fetchall()
                    data.writerow([day, i, j, int(answer[0][0]), int(answer[0][1])])
    # close the DB connection
    conn.close()

## Drop table.
#
# @param dbname name of the database
# @param user name of the user, make ensure user has access to the database!
# @param host name (if the database is local, just 'localhost')
# @param password of the database user
# @param name of the table
def dropTable(dbname, user, host, password, name):
    # connect to DB
    conn = db.connect("dbname=%s user=%s host=%s password=%s" % (dbname, user, host, password))
    # fetch the cursor
    cur = conn.cursor()
    cur.execute("""DROP TABLE %s""" % (name))
    # commit changes
    conn.commit()
    # close the DB connection
    conn.close()

# try to remove the CSV file
try:
    remove("%s/%s/%s.csv" % (DIRECTORY, "dbTestOutput", TESTTABLENAME))
except:
    pass

try:
    save(DBNAME, USERNAME, HOST, PASSWORD, "%s/dbTestOutput" % (DIRECTORY),
         TESTTABLENAME, 10, 10, 1)
except:
    pass

try:
    dropTable(DBNAME, USERNAME, HOST, PASSWORD, TESTTABLENAME)
except:
    pass

print("Saved content of table %s to CSV." % (TESTTABLENAME))