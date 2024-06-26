import json
from datetime import datetime, time


class GetOrSetRedisData:
    """
        Helper class to get and set data in Redis.
    """

    @staticmethod
    async def get(conn, key):
        """
            Retrieve data from Redis.

            Args:
               conn: Redis connection object.
               key: Key to retrieve data from Redis.

            Returns:
               dict or None: Decoded JSON data if key exists, None if key doesn't exist.
        """
        data = conn.get(key)
        if data is None:
            return None
        return json.loads(data)

    @staticmethod
    async def set(conn, key, data):
        """
            Store data in Redis.

            Args:
               conn: Redis connection object.
               key: Key to store data in Redis.
               data: Data to be stored (should be JSON-serializable).
        """
        conn.set(key, json.dumps(data).encode('utf-8'))


class TimeFormatConversion:
    """
        Helper class to convert time string to datetime object.
    """

    @staticmethod
    async def convert_time(value):
        """
            Converts a datetime.time object to another datetime.time object.

            Args:
                value (time): The datetime.time object to convert.

            Returns:
                time: The converted datetime.time object.
        """
        if isinstance(value, time):
            value = datetime.strptime(value.strftime("%H:%M:%S"), "%H:%M:%S").time()
            return value

    @staticmethod
    async def convert_and_format_time(time_value):
        """
            Converts a datetime.time object to ISO 8601 format.

            Args:
                time_value (time): The datetime.time object to convert.

            Returns:
                str: ISO 8601 formatted string representing the time, or None if time_value is None.
        """
        if time_value:
            converted_time = await TimeFormatConversion().convert_time(time_value)
            return converted_time.isoformat() if converted_time else None
        return None


class RedisDataValidator:
    """
        Utility class for validating data in a Redis database.

        Methods:
            validate_data(connection, key, validate_value, exclude_redis_key=None):
                Validates if a specified value exists in the Redis database under a given key,
                optionally excluding a specific Redis key.

            Args:
            connection (redis.Redis): The Redis connection object.
            key (str): The key to look for within each Redis value.
            validate_value (str): The value to validate existence within Redis.
            exclude_redis_key (str, optional): The Redis key to exclude from validation.

            Returns:
                bool: True if the validate_value exists in any Redis value under the specified key,
                      False otherwise.
    """

    @staticmethod
    async def validate_data(connection, key, validate_value, exclude_redis_key=None):
        """
            Validate if a value exists in the Redis database under a given key.

            Args:
                connection (redis.Redis): The Redis connection object.
                key (str): The key to look for within each Redis value.
                validate_value (str): The value to validate existence within Redis.
                exclude_redis_key (str, optional): The Redis key to exclude from validation.

            Returns:
                bool: True if the validate_value exists in any Redis value under the specified key,
                      False otherwise.
        """
        redis_keys = connection.keys('*')

        # Exclude the specified key
        if exclude_redis_key:
            keys = [redis_key for redis_key in redis_keys if redis_key != exclude_redis_key.encode()]

        redis_values = connection.mget(redis_keys)
        values = [json.loads(redis_value).get(key) for redis_value in redis_values]

        if validate_value in values:
            return True
