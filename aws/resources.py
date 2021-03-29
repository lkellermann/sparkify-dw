from abc import ABCMeta, abstractmethod
import boto3


class ResourceFactory(metaclass=ABCMeta):
    """Metaclass to create Resources for AWS."""

    @abstractmethod
    def resource(self):
        pass


class CreateResource(ResourceFactory):
    """Creates Resources for AWS."""

    def resource(self):
        return Resource


class Resource(CreateResource):
    """Creates Resources for AWS."""

    def __init__(self,
                 key_id: str,
                 secret: str,
                 region: str,
                 resource_type: str) -> None:
        """Object constructor.

        Args:
            key_id (str): Key ID to create IAM role.
            secret (str): Secret ID to create IAM role.
            region (str): Region name.
            type (str): Type of client to be created.
        """
        self.key_id = key_id
        self.secret = secret
        self.region = region
        self.resource_type = resource_type

    def resource(self) -> boto3.session.Session.resource:
        """Method to create a Resource instance in AWS.

        Returns:
            object: Resource instance.
        """
        print(
            f'Resource type: {self.resource_type}.\nResource region: {self.region}')
        resource = boto3.resource(self.resource_type,
                                  aws_access_key_id=self.key_id,
                                  aws_secret_access_key=self.secret,
                                  region_name=self.region
                                  )

        return resource


class EC2(Resource):
    """Creates an EC2 Resource instance."""

    def __init__(self,
                 key_id: str,
                 secret: str,
                 region: str,
                 ) -> None:
        """Class constructor.

        Args:
            key_id (str): Key ID to create IAM role.
            secret (str): Secret ID to create IAM role.
            region (str): Region name.
        """
        Resource.__init__(self,
                          key_id,
                          secret,
                          region,
                          resource_type='ec2')
        return None

    def ec2(self) -> boto3.session.Session.resource:
        """Method to create an EC2 Resource instance in AWS.

        Returns:
            boto3.session.Session.resource: Returns an EC2 Resource instance.
        """
        return self.resource()


class S3(Resource):
    """Creates a S3 Resource instance."""

    def __init__(self,
                 key_id: str,
                 secret: str,
                 region: str,
                 ) -> None:
        """Class constructor.

        Args:
            key_id (str): Key ID to create IAM role.
            secret (str): Secret ID to create IAM role.
            region (str): Region name.
        """

        Resource.__init__(self,
                          key_id,
                          secret,
                          region,
                          resource_type='s3')

        return None

    def s3(self) -> boto3.session.Session.resource:
        """Method to create a S3 Resource instance in AWS.

        Returns:
            boto3.session.Session.resource: Returns a S3 Resource instance.
        """
        return self.resource()
