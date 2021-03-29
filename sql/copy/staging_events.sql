copy staging_events from 's3://udacity-dend/log_data'
    credentials 'aws_iam_role={role_arn}'
    compupdate off statupdate off
    region 'us-west-2' format as JSON 's3://udacity-dend/log_json_path.json'
    timeformat as 'epochmillisecs';