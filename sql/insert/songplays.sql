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