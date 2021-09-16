### CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirement
 * Data Files
 * Staging Tables
 * Data Modeling
 * ETL Pipeline
 * Project Workspace
 * instructions 


 
### INTRODUCTION 

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app

### REQUIREMENTS 

Building an ETL pipeline that extracts Sparkify data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

### DATA FILES

* **Song Dataset**.
    is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.


* **Log Dataset**.
     consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

### STAGING TABLES

* **staging_events Table**.
        contains Log_data files' data


* **staging_songs Table**.
        contains song_data files' data

### DATA MODELING.

**Schema for Song Play Analysis:**  
Using the song and log datasets, I have created Data Warehouse using star schema in Redshift in the cloud to be optimized for queries on song play analysis. This includes the following tables.

**Fact Table**
* **songplays** - records in log data associated with song plays i.e. records with page NextSong.
    * **Columns**: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent.
    
**Dimension Tables**
* **users** - users in the app.
    * **Columns**: user_id, first_name, last_name, gender, level    
* **songs** - songs in music database
    * **Columns**: song_id, title, artist_id, year, duration    
* **artists** - artists in music database.
    * **Columns**: artist_id, name, location, latitude, longitude.
* **time** - timestamps of records in songplays broken down into specific units.
    * **Columns**: start_time, hour, day, week, month, year, weekday.
    
### ETL PIPELINE  
1. load data from S3 to staging tables on Redshift..
2. load data from staging tables to analytics tables on Redshift. 


### PROJECT WORKSPACE

1. **create_tables.py**: is where you'll create your fact and dimension tables for the star schema in Redshift.
2. **etl.py**:is where you'll load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.
3. **sql_queries.py**: contains SQL statements, which will be imported into the two other files above.


### INSTRUCTIONS

1. Launch a redshift cluster and create an IAM role that has read access to S3.
2. Add redshift database and IAM role info to **dwh.cfg**.
3. run **create_tables.py** whenever you want to create or reset your database and test your ETL pipeline.
4. run **etl.py** to load data from S3 to staging tables on Redshift and transfer data from Staging Tables to Songs Data Warehouse