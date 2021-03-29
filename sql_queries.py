import pathlib
import configparser

# Job parent path:
path = pathlib.Path.cwd()

# DWH configuration
config = configparser.ConfigParser()
config.read('dwh.cfg')


def read_files(kind: str) -> list:
    """Reads query from file.

    Args:
        kind (str): read queries from `create`, `insert` or `copy`\
             subdirectory.

    Returns:
        list: list of strings which contains the queries.
    """
    query_list = []

    files = {'create': ['sql/create/staging_events.sql',
                        'sql/create/staging_songs.sql',
                        'sql/create/time.sql',
                        'sql/create/users.sql',
                        'sql/create/songs.sql',
                        'sql/create/artists.sql',
                        'sql/create/songplays.sql',
                        ],
             'insert': ['sql/insert/time.sql',
                        'sql/insert/users.sql',
                        'sql/insert/songs.sql',
                        'sql/insert/artists.sql',
                        'sql/insert/songplays.sql',
                        ],
             'copy': ['sql/copy/staging_events.sql',
                      'sql/copy/staging_songs.sql'
                      ]
             }

    for file in files[kind]:

        with open(f'{path}/{file}', 'r') as f:
            query = f.read()

        if kind == 'copy':
            query = query.format(role_arn=config['IAM_ROLE']['ARN'])
        query_list.append(query)

    return query_list


# DROP TABLES
staging_events_table_drop = "drop table if exists staging_events cascade;"
staging_songs_table_drop = "drop table if exists staging_songs cascade;"
songplay_table_drop = "drop table if exists songplays cascade;"
user_table_drop = "drop table if exists users cascade;"
song_table_drop = "drop table if exists songs cascade;"
artist_table_drop = "drop table if exists artists cascade;"
time_table_drop = "drop table if exists time;"

# ROW COUNT (RC)
rc_staging_events = "select count(*) from staging_events;"
rc_staging_songs = "select count(*) from staging_songs;"
rc_time = "select count(*) from time"
rc_users = "select count(*) from users; "
rc_artists = "select count(*) from artists;"
rc_songs = "select count(*) from songs;"
rc_songplays = "select count(*) from songplays"


# QUERY LISTS
create_table_queries = read_files('create')
insert_table_queries = read_files('insert')
copy_table_queries = read_files('copy')

drop_table_queries = [staging_events_table_drop,
                      staging_songs_table_drop,
                      songplay_table_drop,
                      user_table_drop,
                      song_table_drop,
                      artist_table_drop,
                      time_table_drop]

rc_queries = [rc_staging_events,
              rc_staging_songs,
              rc_time,
              rc_users,
              rc_artists,
              rc_songs,
              rc_songplays]
