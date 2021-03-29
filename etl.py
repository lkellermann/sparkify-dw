'''
Author: Leandro Kellermann de Oliveira <kellermann@alumni.usp.br>
Date:   2021-03-20 09:00:26
Last modified by:   Leandro Kellermann de Oliveira <kellermann@alumni.usp.br>
Last modified: 2021-03-27 23:58:35
myProjects <<MIT>>
'''
import psycopg2
import configparser
from datetime import datetime
from sql_queries import copy_table_queries, insert_table_queries, rc_queries


def load_staging_tables(cur) -> None:
    """Method to create staging tables

    Args:
        cur ([type]): psycopg cursor to execute queries.
    """
    for query in copy_table_queries:
        print(
            f'Copying table:\n############\nExecuting query:\n{query}\n###########\n\n')
        cur.execute(query)


def insert_tables(cur) -> None:
    """Method to insert data into provided tables tables.

    Args:
        cur ([type]): psycopg2 cursor object to execute queries.
    """
    for query in insert_table_queries:
        print(
            f'Insert tables:\n############\nExecuting query:\n{query}\n###########\n\n')
        cur.execute(query)


def check(cur, start_time):
    """Method to check the number of rows inserted on tables in this project.

    Args:
        cur ([type]): psycopg2 cursor object to execute queries.
        start_time ([type]): datetime object of time when etl.py started.
    """
    for query in rc_queries:
        now = datetime.now()
        cur.execute(query)
        results = cur.fetchone()
        txt = f'{now} Count #rows:\n############\nQuery: {query}\nResults{results}\n############\n\n'
        print(txt)
        strf = start_time.strftime("%Y%m%d%H%M%S")
        with open(f"etl_{strf}.results", 'a') as f:
            f.write(txt)


def main():
    """Main method to execute ETL operations."""

    start_time = datetime.now()

    # Get data warehouse access information:
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # Try to connect to cluster
    con = psycopg2.connect("host={} \
                            dbname={} \
                            user={} \
                            password={} \
                            port={}".format(*config['CLUSTER'].values()))

    con.set_session(autocommit=True)
    cur = con.cursor()

    load_staging_tables(cur)
    insert_tables(cur)
    endpoint = config['CLUSTER']['HOST']
    print(f'DW created on {endpoint}!')
    print('Checking results..\n')

    check(cur, start_time)

    cur.close()
    con.close()
    print('\n\nEnd of execution!')


if __name__ == "__main__":
    main()
