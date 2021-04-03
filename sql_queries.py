import pathlib
import configparser

# Job parent path:
path = pathlib.Path.cwd()

# DWH configuration
config = configparser.ConfigParser()
config.read('dwh.cfg')


# CREATE QUERIES:
create_staging_events = """
create table if not exists staging_events(
    artist              varchar,
    auth                varchar,
    firstName           varchar,
    gender              varchar,
    itemInSession       smallint,
    lastName            varchar,
    length              real,
    level               varchar,
    location            varchar,
    method              varchar,
    page                varchar,
    registration        real,
    sessionId           int,
    song                varchar,
    status              int,
    ts                  timestamp,
    userAgent           varchar,
    userId              int
);
"""
create_staging_songs = """
create table if not exists staging_songs(
    num_songs           int,
    artist_id           varchar sortkey distkey,
    artist_latitude     float,
    artist_longitude    float,
    artist_location     varchar,
    artist_name         varchar,
    song_id             varchar ,
    title               varchar,
    duration            real,
    year                smallint
);
"""

create_time = """
create table if not exists time(
	start_time	timestamp distkey sortkey primary key
	,hour 		smallint
	,day 		smallint
	,week 		smallint
	,month 		smallint
	,year 		smallint
	,weekday 	smallint
);
"""

create_users = """
create table if not exists users(
	user_id		int	distkey sortkey primary key
	,first_name	varchar not null
	,last_name	varchar not null
	,gender 	varchar
	,level 		varchar
);
"""

create_songs = """
create table if not exists songs(
	song_id 	varchar(30) distkey primary key
	,title 		varchar not null
	,artist_id 	varchar(30) not null  
	,year 		smallint
	,duration 	real not null
);
"""

create_artists = """
create table if not exists artists(
	artist_id 	varchar(30) distkey primary key
	,name 		varchar not null
	,location 	varchar
	,latitude 	float
	,longitude 	float
);
"""

create_songplays = """
create table if not exists songplays(
	songplay_id	int		identity(0,1)	primary key
	,start_time	timestamp	not null	references time(start_time)
	,user_id	int		not null	references users(user_id)
	,level		varchar
	,song_id	varchar(30)	not null	references songs(song_id)
	,artist_id	varchar(30)	not null	references artists(artist_id)
	,session_id	int
    ,location	varchar
    ,user_agent	varchar
);
"""

# COPY QUERIES:
copy_staging_events = """
copy staging_events from 's3://udacity-dend/log_data'
    credentials 'aws_iam_role={role_arn}'
    compupdate off statupdate off
    region 'us-west-2' format as JSON 's3://udacity-dend/log_json_path.json'
    timeformat as 'epochmillisecs';
"""

copy_staging_songs = """
copy staging_songs from 's3://udacity-dend/song_data'
	credentials 'aws_iam_role={role_arn}'
	compupdate off statupdate off
	region 'us-west-2' format as JSON 'auto';
"""


# INSERT QUERIES:
insert_time = """
insert into time(start_time
				,hour
				,day
				,week
				,month
				,year
				,weekday
)

select a.ts as start_time
	,extract(hour from a.ts) as hour
	,extract(day from a.ts) as day
	,extract(week from a.ts) as week
	,extract(month from a.ts) as month
	,extract(year from a.ts) as year
	,extract(dayofweek from a.ts ) as weekday
	from(
		select distinct ts
			from staging_events
		) a;
"""

insert_users = """
insert into users(user_id
				,first_name
                ,last_name
                ,gender
                ,level
				)
select distinct
		a.userid as user_id
        ,a.firstName AS first_name
        ,a.lastName  AS last_name
        ,a.gender
        ,a.level
    from(select userid
	        ,firstName
    	    ,lastName
        	,gender
        	,level
		from staging_events
		where userid is not null
			and page = 'NextSong') a;
"""

insert_songs = """
insert into songs(song_id
				,title
				,artist_id
				,year
				,duration
)
select distinct
	a.song_id
	,a.title
	,a.artist_id
	,a.year
	,a.duration
from(select song_id
			,title
			,artist_id
			,year
			,duration
	from staging_songs
	where song_id is not null) a;
"""

insert_artists = """
insert into artists(artist_id
                    ,name
                    ,location
                    ,latitude
                    ,longitude
                    )
select distinct
		a.artist_id 
		,a.artist_name        as name
        ,a.artist_location    as location
        ,a.artist_latitude    as latitude
        ,a.artist_longitude   as longitude
 from (select artist_id 
		    ,artist_name
            ,artist_location
            ,artist_latitude
            ,artist_longitude
 	from staging_songs 
 		where artist_id is not null) a;
"""

insert_songplays = """
insert into songplays(
	start_time
	,user_id
	,level
	,song_id
	,artist_id
	,session_id
	,location
	,user_agent
	)
select	se.ts as start_time 
        ,se.userid as user_id 
        ,se.level 
        ,ss.song_id 
        ,ss.artist_id 
        ,se.sessionId     AS session_id
        ,se.location 
        ,se.userAgent     AS user_agent
 from staging_events se, staging_songs ss
 where se.page = 'NextSong'
 	and se.song = ss.title
 	and se.userid not in (
 					-- Avoid loading the same register twice.
 					select distinct
                		sp.user_id 
			            FROM songplays sp 
            		    	WHERE sp.user_id is not null 
            		    	and sp.user_id = se.userId
            		    	and sp.session_id = se.sessionId
            		    	and sp.user_id in (select user_id from users));
"""


# DROP TABLES QUERIES
staging_events_table_drop = "drop table if exists staging_events cascade;"
staging_songs_table_drop = "drop table if exists staging_songs cascade;"
songplay_table_drop = "drop table if exists songplays cascade;"
user_table_drop = "drop table if exists users cascade;"
song_table_drop = "drop table if exists songs cascade;"
artist_table_drop = "drop table if exists artists cascade;"
time_table_drop = "drop table if exists time;"

# ROW COUNT (RC) QUERIES
rc_staging_events = "select count(*) from staging_events;"
rc_staging_songs = "select count(*) from staging_songs;"
rc_time = "select count(*) from time"
rc_users = "select count(*) from users; "
rc_artists = "select count(*) from artists;"
rc_songs = "select count(*) from songs;"
rc_songplays = "select count(*) from songplays"


# CREATE TABLE QUERIES LIST:
create_table_queries = [create_staging_events,
                        create_staging_songs,
                        create_time,
                        create_users,
                        create_songs,
                        create_artists,
                        create_songplays,
                        ]

# COPY TABLE QUERIES LIST:
copy_table_queries = [copy_staging_events,
                      copy_staging_songs,
                      ]

# INSERT TABLE QUERIES LIST:
insert_table_queries = [insert_time,
                        insert_users,
                        insert_songs,
                        insert_artists,
                        insert_songplays,
                        ]

# DROP TABLE QUERIES LIST:
drop_table_queries = [staging_events_table_drop,
                      staging_songs_table_drop,
                      songplay_table_drop,
                      user_table_drop,
                      song_table_drop,
                      artist_table_drop,
                      time_table_drop]
# ROW COUNT QUERIES LIST:
rc_queries = [rc_staging_events,
              rc_staging_songs,
              rc_time,
              rc_users,
              rc_artists,
              rc_songs,
              rc_songplays]
