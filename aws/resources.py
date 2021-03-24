from abc import ABCMeta, abstractmethod
import boto3


class ResourceFactory(metaclass=ABCMeta):
    """Metaclass to create Resources for AWS.

    Args:
        metaclass ([type], optional): [description]. Defaults to ABCMeta.
    """
    @abstractmethod
    def resource(self):
        pass


class CreateResource(ResourceFactory):
    """Creates Resources for AWS."""

    def resource(self):
        return Resource()


class Resource(CreateResource):
    """Creates Resources for AWS."""

    def __init__(self,
                 key_id: str,
                 secret: str,
                 token: str,
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
        self.token = token
        self.region = region
        self.resource_type = resource_type

    def resource(self) -> object:
        """Method to create a Resource instance in AWS.

        Returns:
            object: Resource instance.
        """
        # print(f"""self.key_id = {self.key_id}
        #self.secret = {self.secret}
        #self.token = {self.token}
        #self.region = {self.region}
        #self.resource_type = {self.resource_type}
        # """)
        resource = boto3.resource(self.resource_type,
                                  aws_access_key_id=self.key_id,
                                  aws_secret_access_key=self.secret,
                                  aws_session_token=self.token,
                                  region_name=self.region
                                  )

        return resource


class EC2(Resource):
    """Creates an EC2 Resource instance."""

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
            region (str): Region name.
        """
        Resource.__init__(self,
                          key_id,
                          secret,
                          token,
                          region,
                          resource_type='ec2')
        return None

    def ec2(self) -> object:
        """Method to create an EC2 Resource instance in AWS.

        Returns:
            object: Returns an EC2 Resource instance.
        """
        print('Going to create an EC2 instance.')
        return self.resource()


class S3(Resource):
    """Creates a S3 Resource instance."""

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
            region (str): Region name.
        """

        Resource.__init__(self,
                          key_id,
                          secret,
                          token,
                          region,
                          resource_type='s3')

        return None

    def s3(self) -> object:
        """Method to create a S3 Resource instance in AWS.

        Returns:
            object: Returns a S3 Resource instance.
        """
        return self.resource()
