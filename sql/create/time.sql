create table if not exists time(
	start_time	timestamp distkey sortkey primary key
	,hour 		smallint
	,day 		smallint
	,week 		smallint
	,month 		smallint
	,year 		smallint
	,weekday 	smallint
);