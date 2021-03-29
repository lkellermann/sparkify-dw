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
	 
