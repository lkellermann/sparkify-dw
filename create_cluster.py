'''
Author: Leandro Kellermann de Oliveira <kellermann@alumni.usp.br>
Date:   2021-03-29 08:07:45
Last modified by:   Leandro Kellermann de Oliveira <kellermann@alumni.usp.br>
Last modified: 2021-03-29 08:07:45
myProjects <<license>>
'''
import yaml
import configparser
import os
from aws.redshift_cluster import Cluster


def main() -> None:
    """Method to create a RedShift cluster, open its VPC\
         and return the dwh.cfg file for later access.
    """
    # Reads YAML file which contains the RedShift
    # cluster creation parameters.
    print('Loading cluster setup from setup.yaml file.')
    with open("setup.yaml", 'r') as stream:
        setup = yaml.safe_load(stream)

    # Instantiates Cluster object:
    red = Cluster(setup['AWS']['KEY'],
                  setup['AWS']['SECRET'],
                  setup['AWS']['REGION'],
                  setup['CLUSTER']['CLUSTER_IDENTIFIER']
                  )

    # Creates RedShift cluster if does not exists:
    red.create_cluster(setup['CLUSTER']['CLUSTER_TYPE'],
                       setup['CLUSTER']['NUM_NODES'],
                       setup['CLUSTER']['NODE_TYPE'],
                       setup['CLUSTER']['CLUSTER_DB_NAME'],
                       setup['CLUSTER']['DB_USER'],
                       setup['CLUSTER']['DB_PASSWORD'],
                       setup['IAM_ROLE_NAME'],
                       )

    # Open Virtual Private Cloud if is not already open:
    red.ec2_redshift_connection(setup['CLUSTER']['CLUSTER_PORT'])

    # Get RedShift cluster properties:
    prop = red.cluster_properties
    print(prop)

    # Get RedShift Cluster endpoint address:
    endpoint = prop['Endpoint']['Address']

    # Get RedShift cluster associated IAM Role ARN:
    for x in prop['IamRoles']:
        if isinstance(x, dict):
            try:
                iam_arn = x['IamRoleArn']
            except Exception as e:
                print(f'Exception: {e} ')

    # Dump dwh.cfg file:
    config = configparser.ConfigParser()
    config['CLUSTER'] = {}
    config['CLUSTER']['HOST'] = endpoint
    config['CLUSTER']['DB_NAME'] = setup['CLUSTER']['CLUSTER_DB_NAME']
    config['CLUSTER']['DB_USER'] = setup['CLUSTER']['DB_USER']
    config['CLUSTER']['DB_PASSWORD'] = setup['CLUSTER']['DB_PASSWORD']
    config['CLUSTER']['DB_PORT'] = str(setup['CLUSTER']['CLUSTER_PORT'])
    config['IAM_ROLE'] = {}
    config['IAM_ROLE']['ARN'] = iam_arn

    if os.path.exists('dwh.cfg'):
        os.remove('dwh.cfg')

    # Saving parameters into a file:
    with open('dwh.cfg', 'w') as f:
        config.write(f)

    print('Cluster created!')


if __name__ == "__main__":
    main()
