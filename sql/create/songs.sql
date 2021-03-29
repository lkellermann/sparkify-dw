create table if not exists songs(
	song_id 	varchar(30) distkey primary key
	,title 		varchar not null
	,artist_id 	varchar(30) not null  
	,year 		smallint
	,duration 	real not null
);