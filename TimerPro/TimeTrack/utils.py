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
