copy staging_songs from 's3://udacity-dend/song_data'
	credentials 'aws_iam_role={role_arn}'
	compupdate off statupdate off
	region 'us-west-2' format as JSON 'auto';