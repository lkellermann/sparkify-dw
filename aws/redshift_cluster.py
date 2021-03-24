from aws.iam_role import IAMRole
from aws.resources import EC2
#from aws.resources import S3
from aws.client import RedShift
from typing import Union
from time import sleep
import botocore.exceptions


class Cluster(EC2, IAMRole, RedShift):
    """Creates a RedShift cluster."""

    def __init__(self,
                 key_id: str,
                 secret: str,
                 token: str,
                 region: str,
                 CLUSTER_IDENTIFIER: str
                 ) -> None:
        """Class constructor. Build an RedShift client instance.

        Args:
            key_id (str): Key ID to create a RedShift cluster.
            secret (str): Secret ID to create RedShift cluster.
            region (str): Region name.
            s3_role_name (str): Region name.
        """
        IAMRole.__init__(self, key_id, secret, token, region)
       # S3.__init__(self, key_id, secret, token, region)
        EC2.__init__(self, key_id, secret, token, region)
        RedShift.__init__(self, key_id, secret, token, region)

        self.CLUSTER_IDENTIFIER = CLUSTER_IDENTIFIER

    def create_cluster(self,
                       CLUSTER_TYPE: str,
                       NUM_NODES: int,
                       NODE_TYPE: str,
                       # CLUSTER_IDENTIFIER: str,
                       DBASE: str,
                       DBASE_USER: str,
                       DBASE_PWD: int,
                       IAM_ROLE_NAME: str

                       ):

        # Get IAMRole for S3:
        arn = self.read_only(IAM_ROLE_NAME)

        if isinstance(arn, str):
            arn = [arn]
        elif isinstance(arn, list):
            pass

        try:
            # Creates a redshift client:
            response = self.redshift().create_cluster(
                # Cluster Hardware setup:
                ClusterType=CLUSTER_TYPE,
                NodeType=NODE_TYPE,
                NumberOfNodes=NUM_NODES,

                # Authentication:
                DBName=DBASE,
                ClusterIdentifier=self.CLUSTER_IDENTIFIER,
                MasterUsername=DBASE_USER,
                MasterUserPassword=DBASE_PWD,

                # IAMRole for S3 access:
                IamRoles=arn
            )
            print(f'response: {response}')

            while self.cluster_properties['ClusterStatus'] != 'available':
                print('Waiting cluster to be created...')
                sleep(30)

            print('Cluster available!')

            temp_user = cluster_creds['DbUser']
            temp_pswd = cluster_creds['DbPassword']
            print(f'temp_user: {temp_user}\ntemp_pswd: {temp_pswd}')

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ClusterAlreadyExists':
                print(
                    f'Cluster {self.CLUSTER_IDENTIFIER} already exists. Keep working or create a new cluster.')
            else:
                raise e

        cluster_creds = self.redshift().get_cluster_credentials(
            DbUser=DBASE_USER, DbName=DBASE, ClusterIdentifier=self.CLUSTER_IDENTIFIER, AutoCreate=False)

        temp_user = cluster_creds['DbUser']
        temp_pswd = cluster_creds['DbPassword']
        print(f'temp_user: {temp_user}\ntemp_pswd: {temp_pswd}')
        print(f'cluster_creds: {cluster_creds}')
        return None

    # Building cluster_properties attribute.
    @property
    def cluster_properties(self) -> dict:
        """Getter method to generates `cluster_properties` attributes.

        Returns:
            dict: dictionary with cluster properties.
        """
        cluster_properties = self.redshift().describe_clusters(
            ClusterIdentifier=self.CLUSTER_IDENTIFIER)['Clusters'][0]
        return cluster_properties

    def ec2_redshift_connection(self, PORT: int):

        # Open Virtual Private Cloud:
        print('Opening Virtual Private Cloud...')
        ec2 = self.ec2()

        print(f'ec2: {ec2}')
        vpc = ec2.Vpc(id=self.cluster_properties['VpcId'])
        print(f'Virtual Private Cloud open at {vpc}.')

        # Get default security group:
        sec_group = list(vpc.security_groups.all())[0]

        # Authenticates connection through all IPV4:
        try:
            sec_group.authorize_ingress(
                GroupName=sec_group.group_name,
                CidrIp='0.0.0.0/0',
                IpProtocol='TCP',
                FromPort=PORT,
                ToPort=PORT,
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'InvalidPermission.Duplicate':
                print(
                    f'The specified rule "peer: 0.0.0.0/0, TCP, from port: 5439, to port: 5439, ALLOW" already exists.')
            else:
                raise e
        except:
            InvalidPermission.Duplicate

    @staticmethod
    def _redshift_properties(properties):
        keys = ["ClusterIdentifier",
                "NodeType",
                "ClusterStatus",
                "MasterUsername",
                "DBName",
                "Endpoint",
                "NumberOfNodes",
                'VpcId', ]
        _data = [(k, v)
                 for k, v in self.cluster_properties.items() if k in keys]
        return pd.DataFrame(data=_data, columns=['Key', 'Value'])
