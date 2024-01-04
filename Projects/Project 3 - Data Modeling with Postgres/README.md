## Project: Data Modeling with Postgres

-----

### Sparkify the Music Streaming Service
Sparkify is a music streaming app service that wants to analyze the data on songs and user activity. They want to know what songs users are listening to. Currently, there isn't an easy way to get this data. The data resides in a file directory of JSON logs, with metadata on the songs. They need Data Engineers, like us, to create a Postgres database with tables, so we can run queries for data analysis. We'll be creating the necessary database schema and ETL pipelines. Afterwards we'll be able to test the database and ETL pipeline by running queries and matching the results to their expectations.

-----

### Project Description
For this project, we'll be applying our data modeling skills by using a Postgres database and use Python to create our ETL pipeline. We'll create the necessary fact and dimension tables for our star schema database. The data will be transfered from the files within two local directories for the ETL pipeline, using Python and SQL.

------


### Project Files
The folders and files needed for the project:

* /data/song_data = folder with JSON song data files
* /data/log_data = folder with JSON log data files

* create_tables.py = Use to DROP and CREATE tables. **Note:** Run in order to reset tables prior to running ETL scripts.
* etl.py = Use to read and process files from song_data and log_data; Loads them into tables. You can use the ETL notebook to fill out the script.
* sql_queries.py = Use as a repository for project sql queries.
* etl.ipynb = Use to read and process a single file from song_data and log_data; Load them into tables. The notebook contains instructions on the ETL process for the tables.
* test.ipynb = Use to test and check logic for the database tables.

-----

### Project Steps

* Create tables

    * Write ***CREATE*** statements in the ***sql.queries.py*** to create each table.
    * Write ***DROP*** statements in the ***sql.queries.py*** to drop each table.
    * Run the ***create_tables.py*** to create the database and tables.
    * Run the ***test.ipynb*** to check the creation of the tables with correct column names.


* Build ETL Processes

    * Work through the instructions in the ***etl.ipynb*** notebook to create the necessary
      ETL processes for the tables. Utilize the ***test.ipynb*** notebook to check the records
      successfully inserted in the the tables. Make sure all code runs without error prior to 
      moving forward.


* Build ETL Pipeline

    * Use the python logic that you completed in the ***etl.ipynb*** notebook to complete
      the ***etl.py*** script for the entire dataset. 

***Note:*** You will have to run the ***create_tables.py*** each time prior to running the other files ***(test.ipynb, etl.ipynb, etl.py)***. An at least once to create the actual sparkifydb database.

-----

### Sparkify Database (Star Schema)

The Sparkify Database is based on a Star Schema with a total of (5) tables. (1) Fact table and (4) Dimension tables.

* Fact table
    * songplays
* Dimension tables
    * songs
    * artists
    * users
    * time

Each table contains the necessary primary and foreign key attributes for referential integrity. This is the best design
for this project. All columns and data types are included based on the information we provided within the ***CREATE***
table properties, as part of the ***sql_queries.py***.

-----

### Summary

After you have sucessfully ran all the necessary python and notebook objects, hopefully everyhting checks out, as expected. This is analysis
provides a wealth of information that Sparkify can now use to study activity on their music app, as it relates to song usage.



