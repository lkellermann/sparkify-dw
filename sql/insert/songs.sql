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
