import psycopg2
import configparser
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur) -> None:
    """Method to drop tables that currently exists."""
    for query in drop_table_queries:
        print(query)
        cur.execute(query)


def create_tables(cur) -> None:
    """Method to create staging and dimensional tables."""
    for query in create_table_queries:
        print(f'{query}\n')
        cur.execute(query)


def main():
    """Method to create database and tables based on defined queries."""
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    con = psycopg2.connect("host={} dbname={}\
         user={} password={} port={}".format(*config['CLUSTER'].values()))
    con.set_session(autocommit=True)
    cur = con.cursor()

    drop_tables(cur)
    create_tables(cur)

    cur.close()
    con.close()
    print('End of create_tables.py')


if __name__ == "__main__":
    main()
