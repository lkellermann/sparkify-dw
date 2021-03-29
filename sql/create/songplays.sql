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