import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

#--------------
# DROP TABLES
#--------------
#1-Drop staging Tables
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"

#2-Drop Fact table
songplay_table_drop = "DROP TABLE IF EXISTS songplay"

#3-Drop Dimention Tables
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

#--------------
# CREATE TABLES
#---------------
# 1-Create Staging Tables
staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS staging_events
                                    ( 
                                        event_id INT IDENTITY(0,1) PRIMARY KEY,
                                        artist VARCHAR,
                                        auth VARCHAR,
                                        firstName VARCHAR,
                                        gender VARCHAR,
                                        itemInSession INT,
                                        lastName VARCHAR,
                                        length FLOAT,
                                        level VARCHAR,
                                        location VARCHAR,
                                        method VARCHAR,
                                        page VARCHAR,
                                        registration FLOAT,
                                        sessionId INT,
                                        song VARCHAR,
                                        status INT,
                                        ts BIGINT,
                                        userAgent TEXT,
                                        userId INT
                                    )

""")


staging_songs_table_create= (""" CREATE TABLE IF NOT EXISTS staging_songs
                                    (
                                        num_songs INT,
                                        artist_id VARCHAR,
                                        artist_latitude VARCHAR,
                                        artist_longitude VARCHAR,
                                        artist_location VARCHAR,
                                        artist_name VARCHAR,
                                        song_id VARCHAR PRIMARY KEY,
                                        title VARCHAR,
                                        duration FLOAT,
                                        year INT
                                    )
""")

# 2-Create Fact Table
songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays 
                                (
                                    songplay_id INT IDENTITY(0,1) PRIMARY KEY ,
                                    start_time TIMESTAMP NOT NULL,
                                    user_id int NOT NULL distkey,
                                    level varchar,
                                    song_id varchar ,
                                    artist_id varchar,
                                    session_id int,
                                    location varchar,
                                    user_agent varchar
                                ) 

""")
# 3-Create Dimension Tables
user_table_create = ("""CREATE TABLE IF NOT EXISTS users
                             (
                                user_id int PRIMARY KEY,
                                first_name varchar,
                                last_name varchar,
                                gender varchar,
                                level varchar
                             )
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs
                            (
                                song_id varchar PRIMARY KEY distkey,
                                title varchar,
                                artist_id varchar NOT NULL,
                                year int,
                                duration float
                            )
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists
                            (
                                artist_id varchar PRIMARY KEY,
                                name varchar,
                                location varchar,
                                latitude varchar,
                                longitude varchar
                            )
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time
                        (
                            start_time TIMESTAMP PRIMARY KEY,
                            hour int,
                            day int,
                            week int,
                            month int,
                            year int,
                            weekday varchar
                        )
""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events 
                            from {} credentials  
                            'aws_iam_role={}'   
                            json {}  
                            compupdate off
                            region 'us-west-2';
""").format(config.get("S3","LOG_DATA"), config.get("IAM_ROLE", "ARN"), config.get("S3", "LOG_JSONPATH"))

staging_songs_copy = ("""copy staging_songs 
                            from {} credentials  
                            'aws_iam_role={}'   
                            JSON 'auto' truncatecolumns  
                            compupdate off
                            region 'us-west-2';
""").format(config.get("S3","SONG_DATA"), config.get("IAM_ROLE", "ARN"))

#-----------------
# FINAL TABLES
#-----------------

# 1-Fact Table
songplay_table_insert = ("""INSERT INTO songplays(
                                                    start_time,
                                                    user_id,
                                                    level,
                                                    song_id,
                                                    artist_id,
                                                    session_id,
                                                    location,
                                                    user_agent
                                                    )
                           SELECT DISTINCT TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' as start_time,
                                  userId,level,song_id,artist_id,sessionId, location,userAgent
                           FROM staging_events e LEFT JOIN staging_songs s 
                           on e.song = s.title and
                              e.length = s.duration and
                              e.artist= s.artist_name
                           WHERE e.page = 'NextSong' 
                        
""")

# 2-Dimension Tables
user_table_insert = ("""INSERT INTO users
                            (
                                user_id,
                                first_name,
                                last_name,
                                gender,
                                level 
                            )
                    SELECT DISTINCT userId,firstName, lastName, gender,level 
                    FROM staging_events
                    WHERE userId IS NOT NULL and page='NextSong'
                    

""")

song_table_insert = ("""INSERT INTO songs(
                                            song_id,
                                            title,
                                            artist_id,
                                            year,
                                            duration
                                            ) 
                        SELECT DISTINCT song_id, title, artist_id, year, duration 
                        FROM staging_songs

""")


artist_table_insert = ("""INSERT INTO artists (
                                                artist_id,
                                                name,
                                                location,
                                                latitude,
                                                longitude 
                                                ) 
                        SELECT DISTINCT artist_id,artist_name,artist_location,artist_latitude,artist_longitude 
                        FROM staging_songs

""")


time_table_insert = ("""INSERT INTO time (
                                            start_time,
                                            hour,
                                            day,
                                            week,
                                            month,
                                            year,
                                            weekday
                                        )
                            SELECT start_time, 
                            EXTRACT(hour FROM start_time),
                            EXTRACT(day FROM start_time),
                            EXTRACT(week FROM start_time),
                            EXTRACT(month FROM start_time),
                            EXTRACT(year FROM start_time),
                            TO_CHAR( start_time , 'Day') AS "Day"
                            FROM(
                            SELECT DISTINCT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time 
                            FROM staging_events
                            WHERE page='NextSong'
                            ) as t
                            
""")

#------------
# QUERY LISTS
#------------

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
