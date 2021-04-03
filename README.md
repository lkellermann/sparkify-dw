<p align="center">
  <a href="" rel="noopener">
 <img src=img/sparkify_cloud_white_bkgrd.jpg alt="Project logo"></a>
</p>

<h3 align="center">AWS RedShift Data Warehouse</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> This project contain details about creating and modeling the Marketing database on AWS RedShift.
    <br> 
</p>

## 📝**Table of Contents**<a name = "table-of-contents"></a>
---

- [About](#about)
- [Getting Started](#getting_started)
- [Software Requirements](#software_requirements)
- [Installing and Using](#installing_using)
- [Database Model](#dbase_model)
- [Built Using](#built_using)
- [Authors](#authors)

## **About** <a name = "about"></a>
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

Sparkify is becomming popular among population of Oregon region. Because of the large increase in users at our platform we also had to increase our music library. This situation led to an huge growth at `songplays` datamart table that was in [`localhost` in previous years ](https://github.com/kellermann92/sparkify-rdb).


Our main goal with this project is to adapt the previous `songplays` datamart at our `localhost`instance to perform well at AWS RedShift Cluster.To do this migration we developed a simple package named `aws` to help our team to create and access RedShift clusters on AWS.

The table `songplays` is an analytical table that contains information about the users of our platform and the songs they listened to, when, where they were and which kind of device they use to access our platform. This table is useful to get insights to marketing campaings

## 🏁 **Getting Started** <a name = "getting_started"></a>
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

Before starting to run this project you need to fill a `dwh.cfg` file containing the informations about the RedShift cluster that have the `sparkifydw` database, and your database credentials. You will also need the ARN for read the source files from a S3 bucket. Below we provide an example of how the contents of this file should look like:

```
[CLUSTER]
HOST= sparkify-redshift.************.us-west-2.redshift.amazonaws.com
DB_NAME=sparkifydw
DB_USER=s*************r
DB_PASSWORD=S*************r
DB_PORT=5439

[IAM_ROLE]
ARN=arn:aws:iam::************:role/AmazonS3ReadOnlyAccess
```
The `HOST` parameter is the endpoint property of the cluster where the database `DB_NAME` is stored. The parameters `DB_USER` and `DB_PASSWORD` are respectively the database username and it's password.

## **Software requirements**  <a name = "software_requirements"></a>
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

To run the scripts in this repository you will need at least [Python 3.7.X](https://www.python.org/downloads/) and install the packages on `requirements.txt` file in this repository with the following command:

```shell
pip install -f requirements.txt
```

> * We strongly recommend you to run the scripts on a separated Python virtual environment. Click [here](https://docs.python.org/3/tutorial/venv.html) to know more about virtual environments
> * Remember to run the command above with the terminal open at the same directory where the `requirements.txt` file is in.

## **Installing and using** <a name = "installing_using"></a>
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

To install this project you just need to download it.


To execute this project for the first time you need to run the `etl.py` with the following command:

```shell
python etl.py
```

The `etl.py` file will access the file `dwh.cfg` to connect to the database in the provided RedShift cluster and run the queries to create the tables needed, copy the staging tables and insert the data at them. This queries are provided at `sql_queries.py`file.

If the script runs successfully you should see the row counts for each table at the end and also a file named with the pattern `etl_YYYYMMDDHHMMSS.results` containing the results.

## **Database Model** <a name = "dbase_model"></a> 
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

The `songplays` table is generated as illustrated by the ERD bellow:
<p align="center">
  <a href="" rel="songplays_erd">
 <img src=img/songplays_erd.png alt="Songplays ERD."></a>
</p>


The table below presents a brief description of the tables in this project and their respective source and owners.

**Source files and owners**
| Table | Description | Source | Owner |
| ---- | --------- | ---- | ----- |
| `staging_events`| Staging fact table for user events.| `s3://udacity-dend/log_data`| Person 1|
| `staging_songs`| Staging table for song data .| `s3://udacity-dend/song_data` | Person 2|
|`artists`| Dimension table of artists. | `staging_songs`| Person 3
| `songs`| Dimension table for songs.| `staging_songs`| Person 1|
| `time`| Dimension table for time/calendar.| `staging_events`| Person 1|
|`users`| Dimension table for users. | `staging_events` | Person 3|
|`songplays`| Analytical table for recomendation systems. | All above. | Person 2|

## ⛏️ **Built Using** <a name = "built_using"></a>
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

- [Python](https://www.python.org/downloads/)- Programming language.

- [Dbeaver](https://dbeaver.io/) - Database tool.


## ✍️ **Authors** <a name = "authors"></a>
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

- [@kellermann92](https://github.com/kellermann92) - Idea & Initial work.
