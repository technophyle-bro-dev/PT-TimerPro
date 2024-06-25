import os

from dotenv import load_dotenv
from redis import Redis


load_dotenv()


class RedisConnection:
    """
        Establishes a connection to Redis using the provided host and port.

        Attributes:
           redis_client: Redis client instance connected to the specified host and port.
    """

    def __init__(self):
        """
            Initializes a new instance of RedisConnection.

            Creates a Redis client connected to the specified host and port.
        """
        self.redis_client = Redis(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'))
