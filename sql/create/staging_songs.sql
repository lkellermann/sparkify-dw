create table if not exists staging_songs(
    num_songs           int,
    artist_id           varchar sortkey distkey,
    artist_latitude     float,
    artist_longitude    float,
    artist_location     varchar,
    artist_name         varchar,
    song_id             varchar ,
    title               varchar,
    duration            real,
    year                smallint
);