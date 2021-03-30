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
- [Deployment](#deployment)
- [Database Model](#dbase_model)
- [The `aws` API](#aws_api)
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


The dependences to run this project may vary depending if it's being running for the first time for a Cluster or if the cluster already exists.

### **Scenario 1: the cluster does not exist**
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

In this stituation the `etl.py` script will need a `setup.yaml` file containing information about AWS user access able to create the cluster and the database. The `setup.yaml` file must be in the format bellow:

```yaml
AWS:
  KEY: A*****************C2                         # User KEY
  SECRET: Y**************************************C  # User SECRET
  REGION: us-west-2                                 # Choose the region near to our customers.

CLUSTER:
    CLUSTER_TYPE: multi-node
    NUM_NODES: 2
    NODE_TYPE: dc2.large
    CLUSTER_IDENTIFIER: sparkify-redshift     # This is the name of your cluster.
    CLUSTER_PORT: 5439
    CLUSTER_DB_NAME: sparkifydw
    DB_USER: s*************r                  # This is the master username.
    DB_PASSWORD: S*************r              # This is the master password.
    
IAM_ROLE_NAME: AmazonS3ReadOnlyAccess
```
The `AWS KEY` and `AWS SECRET` are provided by the project manager. 
Remember to <font color = 'red'>**keep this parameters with you and only you**</font>. Anyone is allowed to share or ask to share this parameters no matter the role or importance of the people involved.

The `AWS REGION` is fixed as `us-west-2` because it's the region where our access growth and also because it's a cheap reagion to use AWS Cloud resources. See more information about AWS regions, AWS Availability zones and pricing [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html).

The `CLUSTER` hardware configurations here can change depends on how much the `songplays`database will grow. The `CLUSTER_PORT` is setted with the default value. The `CLUSTER_IDENTIFIER` and `CLUSTER_DB_NAME` are respectively the name of the cluster and the name of the first database created on it. These names are in compilance with our XYZ Governance Policy and can't be changed. To know more about the ~~fictional~~ XYZ  Governance Policy click [here](https://www.rd.com/list/short-jokes/).

The `IAM_ROLE_NAME` parameter is an read-only AWS policy to access the `S3` buckets you'll need to access in order to populate the staging tables related to this project. The `S3` address are declared in the `copy` queries at `sql/copy/` directory that populates the `staging_events` and `staging_songs` tables.

The sample of the YAML code above is also provided on `setup.yaml-template` file in this repository.


### **Scenario 2: the cluster already exists**
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

In this scenario you'll need the parameters in a file named `dwh.cfg`. The contents of this file looks like as follows:
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
The `HOST` parameter is the endpoint property of the cluster where the database `DB_NAME` is stored. The parameters `DB_USER` and `DB_PASSWORD` are respectively the database username and it's password. It's not necesserally the same of those defined at `setup.yaml` file. On the other hand the `DB_PORT` parameter is the same value defined on `setup.yaml`.

The `ARN` parameter contains your AWS User ID and is attached to the S3 Read Only policy to get the data to populate taging tables related to this project. The S3 address are declared in the copy queries at sql/copy/ directory that populates the staging_events and staging_songs tables.

The sample of the `cfg` code above is also provided on `dwh.cfg-template` file in this repository.

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


To execute this project for the first time you need to run the scripts in the following order:

```shell
python create_cluster.py
python create_tables.py
python etl.py
```

The script `create_cluster.py` will access the `setup.YAML` file to create a RedShift cluster and also will generates the `dwh.cfg` file needed to run the `create_tables.py` and  `etl.py`scripts. The `create_tables.py` file access `dwh.cfg` to create the connection to the cluster database and the file `sql_queries.py` to get the drop and create queries. The functions to access the `sql` subdirectory are in `sql_queries.py` file aswell. For last `etl.py` file access the  `dwh.cfg` file to connect to the cluster database and get the queries from `sql_queries.py`. After all insert queries are done the row count is provided on the screen and also saved on the main directory  with the pattern name `etl_YYYYMMDDHHMMSS.results`.

If it's not the first time you are running this project, then you can just run the `etl.py` file.


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

## **Subdirectories and their contents**
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

To run this project there are two subdirectories which files are important to run the job properly. They are the `sql` and `aws`.

Each file in `sql` repository contains the query scripts and they are organized based on their function.

In the `copy` folder there are the queries needed to copy the staging tables from their respective `s3` buckets directories.

In the `create` folder we have the queries needed to create the empty tables and their structure. These queries give us the relation among all tables mentioned here.

In the `insert` directory we have the queries to populate the tables through all the pipeline from staging table to the `songplays` table.
```
📦sql
 ┣ 📂copy
 ┃ ┣ 📜staging_events.sql
 ┃ ┗ 📜staging_songs.sql
 ┣ 📂create
 ┃ ┣ 📜artists.sql
 ┃ ┣ 📜songplays.sql
 ┃ ┣ 📜songs.sql
 ┃ ┣ 📜staging_events.sql
 ┃ ┣ 📜staging_songs.sql
 ┃ ┣ 📜time.sql
 ┃ ┗ 📜users.sql
 ┗ 📂insert
 ┃ ┣ 📜artists.sql
 ┃ ┣ 📜songplays.sql
 ┃ ┣ 📜songs.sql
 ┃ ┣ 📜time.sql
 ┃ ┗ 📜users.sql
```

The `aws` subdirectory contains the files needed to run the `aws` API being developed by our team.

The `__init__.py` file is the package constructor. The `client.py`file contains the factory of `boto3.session.Session.client` objects to create the RedShift Cluster and access IAM Role Names and ARNs. In the file `iam_role.py` we implement the contents of `client.py` to create specific roles. In the `redshift_cluster.py` file we implement methods to create a RedShift cluster and get its properties. The `resource.py` file is a factory of `boto3.session.Session.resource` objects that are needed to create and access `S3`buckets and `EC2`instances. The file `aws_uml_file.pyns`is a `Pynsource`file that generates the UML diagram to this API.

```
📦aws
 ┣ 📜THIRD_PARTY_LICENSES
 ┣ 📜__init__.py
 ┣ 📜aws_uml_file.pyns
 ┣ 📜client.py
 ┣ 📜iam_role.py
 ┣ 📜redshift_cluster.py
 ┗ 📜resources.py
```

## **The `aws` API** <a name = "aws_api"></a>
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

The subdirectory `aws` in this repository contains the Python script files that composes the `aws` API to create the cluster in a easy way as you can see in the `create_cluster.py` file. This API and its documentation is under construction but you can see the it's UML diagram and test the features already developed. For more details about an instance of this class you can just run a help command in your Python console:
```python
help(classObject)
```
<p align="center">
  <a href="" rel="aws_uml">
 <img src=img/aws_uml.png alt="UML diagram for aws API."></a>
</p>

## 🚀 **Deployment** <a name = "deployment"></a>
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

You should automate the execution with a task scheduler. This will depend on the operational system where the scripts will run.  

## ⛏️ **Built Using** <a name = "built_using"></a>
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>


- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK.
- [Dbeaver](https://dbeaver.io/) - Database tool.
- [Pynsource](https://www.pynsource.com/) - UML diagrams.

## ✍️ **Authors** <a name = "authors"></a>
---
<small><font color = 'blue'> [📝 Table of Contents](#table-of-contents) </font></a></small>

- [@kellermann92](https://github.com/kellermann92) - Idea & Initial work.
