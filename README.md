# mosquito-simulation

Copyright (C) 2016 flossCoder

This software is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This software is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.

For the GNU GPL 3 see file LICENSE.

This software requires the following programs:
	- Python 3.5.1
	- PostgreSQL 9.5.3
	- PostGIS 2.2
	- Psycopg 2.6.2
	- doxygen (optional for the documentation)

The project contains following folders:
	- run Contains some files for testing. This tests save and load some CSV-files.
			That requires a file tree somewhere on your machine:
			/root
				/applicationTest
				/benchmarkCA
				/benchmarkDB
				/dbTestOutput
				/input (contains some input CSV-file)
				/malcamTest
				/output
			Make sure, that DIRECTORY in setupRun.py saves the path to the root.
			An example file tree (containing the input CSV-files) can be found in
			folder tree.
			Furthermore setupRun.py saves parameter for the database like the name
			of the user. Make sure, that the parameter values are valid.
	- src The source code of the project.
	- test The unittest of the project. Some tests may save or load CSV-files.
			Ensure, that DIRECTORY in setupTests.py is valid.
			Furthermore setupTests.py saves parameter for the database like the name
			of the user. Make sure, that the parameter values are valid.
	- doc The documentation generated with doxygen. And the used Doxyfile.
	- tree An example file tree for the tests in folder run containing some required
			input CSV-files.
