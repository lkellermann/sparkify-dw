create table if not exists users(
	user_id		int	distkey sortkey primary key
	,first_name	varchar not null
	,last_name	varchar not null
	,gender 	varchar
	,level 		varchar
);