# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# dbData.py
# Copyright (C) 2016 flossCoder
# 
# dbData.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# dbData.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package dbData defines the connection to a PostGIS database.

from abstractData import AbstractData
from constants import SRIDUNKNOWN, TYPEDB, XINDEX, YINDEX
import psycopg2 as db
from zeroCA import zeroCA

## DBData defines a CA saving based on a PostGIS database.
class DBData(AbstractData):
    ## init function
    #
    # @param name of the data, will be used as a table name
    # @param coordinateTransformer can transform the internal indexes to real coordinates (used
    # by GIS for example) and vice versa
    # @param dbname name of the database
    # @param user name of the user, make sure user has access to the database!
    # @param host name (if the database is local, just 'localhost')
    # @param password of the database user
    # @param newTable True: create a new table with the given name; False: don't create a new
    #        table
    # @param width number of cells on the abscissa
    # @param height number of cells on the ordinate
    # @param upperleftx x value of the upper left cell
    # @param upperlefty y value of the upper left cell
    # @param scalex pixel size on the abscissa
    # @param scaley pixel size on the ordinate
    # @param skewx rotation of the cells on the abscissa
    # @param skewy rotation of the cells on the ordinate
    # @param srid (spatial reference id) defines the coordinate system
    def __init__(self, name, coordinateTransformer, dbname, user, host, password, newTable,
                 width, height, upperleftx, upperlefty,
                 scalex, scaley, skewx, skewy, srid = SRIDUNKNOWN):
        super().__init__(TYPEDB, name, coordinateTransformer)
        self.__dbname = dbname
        self.__user = user
        self.__host = host
        self.__password = password
        self.__width = width
        self.__height = height
        self.__upperleftx = upperleftx
        self.__upperlefty = upperlefty
        self.__scalex = scalex
        self.__scaley = scaley
        self.__skewx = skewx
        self.__skewy = skewy
        self.__srid = srid
        self.__conn = None
        self.__cur = None
        if newTable:
            # open the connection
            self.__openConnection()
            # create a new table
            self.__createTable()
            # commit changes
            self.__commit()
            # close the database connection
            self.__closeConnection()
    
    
    # public functions (interfaces for the environment)
    
    
    ## Save the given step to all registered elements.
    #
    # @param ca to save
    # @param day to save
    def saveStep(self, ca, day):
        # open the connection
        self.__openConnection()
        # if the day exists in the database, the entry will be overwritten
        if not(self.__existsDay(day)):
            # initialize the day to save
            self.__initDay(day)
        # save the given CA state to the database
        self.__insertDay(ca, day)
        # commit the transaction
        self.__commit()
        # calculate statistics about the content of the table
        self.__analyzeVerbose()
        # close the database connection
        self.__closeConnection()
    
    ## Open a simulation step.
    #
    # @param day of simulation to load
    # @param numx number of cells on abscissa
    # @param numy number of cells on ordinate
    #
    # @return the state of the CA on the given day
    #
    # @exception invalid given day
    def loadStep(self, day, numx, numy):
        # open the connection
        self.__openConnection()
        if not(self.__existsDay(day)):
            raise Exception("No entries for day = %i." % (day))
        # get the CA state
        step = self.__loadDay(day, numx, numy)
        # close the database connection
        self.__closeConnection()
        # return the result
        return step
    
    
    # private internal functions
    
    
    ## Open the database connection and fetch the cursor.
    #
    # @exception Failed to connect to the database.
    # @exception Failed to fetch the cursor.
    def __openConnection(self):
        # connect to the database
        try:
            self.__conn = db.connect("""dbname=%s user=%s host=%s password=%s""" % 
                                     (self.__dbname,
                                      self.__user,
                                      self.__host,
                                      self.__password))
        except:
            raise Exception("""Failed to connect to dbname=%s user=%s host=%s password=%s.""" % 
                            (self.__dbname,
                             self.__user,
                             self.__host,
                             self.__password))
        # fetch the cursor
        try:
            self.__cur = self.__conn.cursor()
        except:
            raise Exception("Failed to fetch the cursor.")
    
    ## Close the database connection.
    #
    # @exception Failed to close the database connection.
    def __closeConnection(self):
        try:
            self.__conn.close()
        except:
            raise Exception("Failed to close the connection.")
    
    ## Create a new table.
    #
    # @param table tableName of the new table.
    #
    # @exception Failed to create the new table.
    # @exception Failed to create a spatial index.
    # @exception Failed to create the non spatial index.
    def __createTable(self):
        # create table
        try:
            self.__cur.execute("""CREATE TABLE %s (
                                    day smallint,
                                    rast raster NOT NULL,
                                    PRIMARY KEY(day));""" % (self._name))
        except:
            self.__closeConnection()
            raise Exception("Failed to create table %s" % (self._name))
        # define index on raster column (http://postgis.net/docs/manual-2.2/using_raster_dataman.html#RT_Raster_Columns)
        try:
            self.__cur.execute("""CREATE INDEX %s_rast_spatial_idx ON %s
            USING gist(ST_ConvexHull(rast));""" % (self._name,
                                                 self._name))
        except:
            self.__closeConnection()
            self.__cur.execute("Failed to create spatial index on table %s." % 
                               (self._name))
        # define index on the days (https://www.postgresql.org/docs/9.1/static/sql-createindex.html and PostgreSQL (Pfeiffer) p. 182)
        try:
            self.__cur.execute("CREATE UNIQUE INDEX %s_day_idx ON %s (day);" % 
                               (self._name,
                                self._name))
        except:
            self.__closeConnection()
            raise Exception("Failed to create index on table %s." % (self._name))
    
    ## Delete the table saved in self._name.
    #
    # @exception Failed to delete the table.
    def __deleteTable(self):
        try:
            self.__cur.execute("DELETE FROM %s;" % (self._name))
        except:
            self.__closeConnection()
            raise Exception("Failed to delete the table %s" % (self._name))
    
    ## Initialize a new day (all adult- and larvae values are zero).
    #
    # @param day to initialize
    #
    # @exception Failed to initialize the given day.
    def __initDay(self, day):
        # initialize entries for new day (all entries are zero)
        try:
            srid = self.__srid
            if (self.__srid == "unknown"):
                # self.__srid == "unknown" => 0
                srid = 0
            
            # http://postgis.net/docs/manual-2.2/RT_ST_MakeEmptyRaster.html
            # http://postgis.net/docs/manual-2.2/RT_ST_AddBand.html
            # PostGIS in action p. 182
            self.__cur.execute("""INSERT INTO %s
                VALUES (%i,
                    ST_AddBand(
                        ST_MakeEmptyRaster(
                            %i,%i,%f,%f,%f,%f,%f,%f,%i
                        ),
                        ARRAY[
                            ROW(1, '32BUI', 0, NULL),
                            ROW(2, '32BUI', 0, NULL)
                        ]::addbandarg[]
                    )
                );""" % 
                (self._name,
                 day,
                 self.__width,
                 self.__height,
                 self.__upperleftx,
                 self.__upperlefty,
                 self.__scalex,
                 self.__scaley,
                 self.__skewx,
                 self.__skewy,
                 srid)
            )
        except:
            self.__closeConnection()
            raise Exception("Failed to initialize day %i." % (day))
    
    ## Update the given value.
    #
    # @param day to update
    # @param band 1: adults, 2: larvae
    # @param coordinates [x, y] coordinates of the cell to update
    # @param value to set
    #
    # @exception Failed to update the given value.
    def __updateValue(self, day, band, coordinates, value):
        try:
            self.__cur.execute("""
                UPDATE %s
                SET rast = ST_SetValue(rast, %i, %i, %i, %i)
                WHERE %s.day = %i;""" % 
                (self._name,
                 band,
                 coordinates[XINDEX],
                 coordinates[YINDEX],
                 value,
                 self._name,
                 day
                 )
            )
        except:
            self.__closeConnection()
            raise Exception("Failed to update day %i at x %i and y %i." % (day,
                                                                         coordinates[XINDEX],
                                                                         coordinates[YINDEX]))
    ## Insert the state of a new day into the database.
    # Precondition: The given day exist in the database.
    #
    # @param ca to save
    # @param day to save
    #
    # @exception Failed to insert the given state.
    def __insertDay(self, ca, day):
        try:
            for i in range(len(ca)):
                for j in range(len(ca[i])):
                    coordinates = self._coordinateTransformer.calcOuterCoordinate(i, j)
                    for n in range(len(ca[i][j])):
                        self.__updateValue(day, (n + 1), coordinates, ca[i][j][n])
        except:
            self.__closeConnection()
            raise Exception("Failed to insert the day %i." % (day))
    
    ## Load the state of a given cell.
    #
    # @param day to load
    # @param coordinates of the cell to load
    #
    # @return state of the given cell [adults, larvae]
    #
    # @exception Failed to load the given cell.
    # @exception Failed to fetch the data from the cursor.
    def __loadCell(self, day, coordinates):
        # load the data
        try:
            self.__cur.execute("""
                SELECT ST_Value(rast, 1, %i, %i) AS adults, ST_Value(rast, 2, %i, %i) AS larvae
                FROM %s
                WHERE %s.day = %i;""" % (coordinates[XINDEX],
                                         coordinates[YINDEX],
                                         coordinates[XINDEX],
                                         coordinates[YINDEX],
                                         self._name,
                                         self._name,
                                         day))
        except:
            self.__closeConnection()
            raise Exception("Failed to load day %i at x %i and y %i." % (day,
                                                                       coordinates[XINDEX],
                                                                       coordinates[YINDEX]))
        # fetch the data from the cursor
        answer = None
        try:
            answer = self.__cur.fetchall()
        except:
            self.__closeConnection()
            raise Exception("Failed to fetch the data from the cursor.")
        return [int(answer[0][0]), int(answer[0][1])]
    
    ## Load the CA state of the given day.
    #
    # @param day to load
    # @param numx the number of cells on the abscissa
    # @param numy the number of cells on the ordinate
    #
    # @return the CA state of the given day
    #
    # @exception Failed to load the given day. 
    def __loadDay(self, day, numx, numy):
        step = zeroCA(2, numx, numy)
        try:
            for i in range(numx):
                for j in range(numy):
                    coordinates = self._coordinateTransformer.calcOuterCoordinate(i, j)
                    data = self.__loadCell(day, coordinates)
                    for n in range(len(data)):
                        step[i][j][n] = data[n]
        except:
            self.__closeConnection()
            raise Exception("Failed to load day %i." % (day))
        return step
    
    ## Check, if the given day exists in the database.
    #
    # @param day to check
    #
    # @return True: if the day exists, False: otherwise
    #
    # @exception Failed to get the count of the given day.
    # @exception Failed to fetch the data from the cursor.
    def __existsDay(self, day):
        # calculate the number of entries for the given day
        try:
            self.__cur.execute("""SELECT COUNT(*) FROM %s WHERE %s.day = %i;""" % 
                               (self._name,
                                self._name,
                                day))
        except:
            self.__closeConnection()
            raise Exception("Failed to get the COUNT of day %i entries." % (day))
        try:
            if (self.__cur.fetchall()[0][0] == 0):
                return False
            else:
                return True
        except:
            self.__closeConnection()
            raise Exception("Failed to fetch the data from the cursor.")
    
    ## Commit the current transaction.
    #
    # @exception Failed to commit the transaction.
    def __commit(self):
        try:
            self.__conn.commit()
        except:
            self.__closeConnection()
            raise Exception("Failed to commit.")
    
    ## Run ANALYZE VERBOSE on the database, which is needed for the index.
    #
    # @exception Failed to ANALYZE VERBOSE.
    def __analyzeVerbose(self):
        try:
            self.__cur.execute("""ANALYZE VERBOSE %s;""" % (self._name))
        except:
            self.__closeConnection()
            raise Exception("Failed to ANALYZE VERBOSE %s." % (self._name))