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
        