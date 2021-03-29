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