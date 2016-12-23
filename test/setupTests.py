# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# setupTests.py
# Copyright (C) 2016 flossCoder
# 
# setupTests.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# setupTests.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package setupTests saves a valid directory to save CSV files and some parameter for the DB

# this directory is used for temporally saving files
DIRECTORY = "/home/bodhi/workspace/mosquito-simulation/test"

# save parameter for the DB
DBNAME = "test" # name of the database
USERNAME = "postgres" # name of the user
HOST = "localhost" # name of the database host
PASSWORD = "bodhi" # password for the user
TESTTABLENAME = "testraster" # name of a n existing table for testing purpose