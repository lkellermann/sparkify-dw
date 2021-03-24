from aws.client import IAM
from typing import Union
import json
import botocore.exceptions


class IAMRole(IAM):
    """Creates IAM Roles."""

    def __init__(self,
                 key_id: str,
                 secret: str,
                 token: str,
                 region: str,
                 ) -> None:
        """Class constructor.

        Args:
            key_id (str): Key ID to create IAM role.
            secret (str): Secret ID to create IAM role.
            token  (str): Session token.
            region (str): Region name.
        """
        IAM.__init__(self,
                     key_id,
                     secret,
                     token,
                     region)
        self.iam = self.iam()
        return None

    def read_only(self, IAM_ROLE_NAME: str) -> Union[str, list]:
        """Method to create and attach an ARN IAM Role.

        Returns:
            str, list: ARN IAM Role.
        """
        try:
            iam = self.iam
            role = iam.create_role(Path='/',
                                   RoleName=IAM_ROLE_NAME,
                                   Description='Allow RedShift Clusters to call AWS resources.',
                                   AssumeRolePolicyDocument=json.dumps(
                                        {
                                            'Statement': [
                                                {
                                                    'Action': 'sts:AssumeRole',
                                                    'Effect': 'Allow',
                                                    'Principal': {
                                                        'Service': 'redshift.amazonaws.com'
                                                    }
                                                }
                                            ],
                                            'Version': '2012-10-17'
                                        }
                                   )
                                   )
            iam.attach_role_policy(RoleName=IAM_ROLE_NAME,
                                   PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess')['ResponseMetadata']['HTTPStatusCode']
            arn = iam.get_role(RoleName=IAM_ROLE_NAME)['Role']['Arn']
            print(f'Role ARN: {arn}')
            return arn
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                arn = iam.get_role(RoleName=IAM_ROLE_NAME)['Role']['Arn']
                print(f'Role already exist: {arn}')
                return arn
            else:
                raise e
