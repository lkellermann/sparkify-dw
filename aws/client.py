from abc import ABCMeta, abstractmethod
import boto3


class ClientFactory(metaclass=ABCMeta):
    """Metaclass to create Clients for AWS.

    Args:
        metaclass ([type], optional): [description]. Defaults to ABCMeta.
    """
    @abstractmethod
    def client(self):
        pass


class CreateClient(ClientFactory):
    """Create Clients for AWS."""

    def client(self) -> object:
        """[summary]

        Returns:
            object: [description]
        """

        return Client()


class Client(CreateClient):
    """Generic class to create Clients for AWS."""

    def __init__(self,
                 key_id: str,
                 secret: str,
                 token: str,
                 region: str,
                 client_type: str) -> None:
        """Object constructor.

        Args:
            key_id (str): Key ID to create an AWS client.
            secret (str): Secret ID to create an AWS client.
            region (str): Region name.
            type (str): Type of client to be created.
        """
        self.key_id = key_id
        self.secret = secret
        self.token = token
        self.region = region
        self.client_type = client_type

    def client(self) -> object:
        """Method to create an AWS client.

        Returns:
            object: AWS Client.
        """
        print(f'Client type: {self.client_type}.\nRegion: {self.region}.')
        client = boto3.client(self.client_type,
                              aws_access_key_id=self.key_id,
                              aws_secret_access_key=self.secret,
                              aws_session_token=self.token,
                              region_name=self.region,
                              )
        return client


class RedShift(Client):
    """Creates a RedShift client."""

    def __init__(self,
                 key_id: str,
                 secret: str,
                 token: str,
                 region: str,
                 ) -> None:
        """Class constructor.

        Args:
            key_id (str): Key ID to create a RedShift client.
            secret (str): Secret ID to create RedShift client.
            region (str): Region name.
        """
        Client.__init__(self,
                        key_id,
                        secret,
                        token,
                        region,
                        client_type='redshift')
        return None

    def redshift(self) -> object:
        """Creates a RedShif client object.

        Returns:
            object: RedShift client object.
        """
        return self.client()


class IAM(Client):
    """Creates IAM in AWS."""

    def __init__(self,
                 key_id: str,
                 secret: str,
                 token: str,
                 region: str,
                 ) -> None:
        """Class constructor.

        Args:
            key_id (str): Key ID to create IAM client.
            secret (str): Secret ID to create IAM client.
            region (str): Region name.
        """
        Client.__init__(self,
                        key_id,
                        secret,
                        token,
                        region,
                        client_type='iam')
        return None

    def iam(self) -> object:
        """Creates an IAM object.

        Returns:
            object: IAM client object.
        """
        return self.client()
