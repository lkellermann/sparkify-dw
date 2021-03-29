create table if not exists artists(
	artist_id 	varchar(30) distkey primary key
	,name 		varchar not null
	,location 	varchar
	,latitude 	float
	,longitude 	float
);