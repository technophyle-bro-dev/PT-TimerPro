import json
import uuid

from starlette.responses import JSONResponse

from TimerPro.TimeTrack.schema import ConfigTimerSchema, UpdateConfigTimerSchema
from TimerPro.TimeTrack.utils import GetOrSetRedisData, TimeFormatConversion
from redis_connection import RedisConnection
from response import APIResponse


class ConfigTimer:
    """
        ConfigTimer handles the setting, getting, and updating of timer configurations in a Redis database.
    """

    def __init__(self):
        """
            Initializes a new instance of ConfigTimer with a connection to the Redis database.
        """
        self.redis_connection = RedisConnection().redis_client

    @staticmethod
    async def set_time_configuration(data: ConfigTimerSchema):
        """
            Sets a new timer configuration in the Redis database.

            Args:
                data (ConfigTimerSchema): The timer configuration data.

            Returns:
                JSONResponse: The response indicating the result of the operation.
        """
        try:
            if data.notify:
                if not data.message:
                    return APIResponse.error_response("Message field is required.", 400)
                if not data.alert_time:
                    return APIResponse.error_response("Alert time field is required.", 400)

            new_data = data.dict()
            new_data['duration'] = await TimeFormatConversion().convert_and_format_time(data.duration)
            new_data['alert_time'] = await TimeFormatConversion().convert_and_format_time(data.alert_time)
            new_data['id'] = str(uuid.uuid4())

            conn = ConfigTimer().redis_connection
            conn.select(1)

            await GetOrSetRedisData().set(conn, new_data.get('id'), new_data)
            return APIResponse.success_response(await GetOrSetRedisData().get(conn, new_data.get('id')),
                                                "Successfully set time configuration.", 200)
        except Exception as e:
            return APIResponse.error_response(str(e), 400)

    @staticmethod
    async def get_time_configuration():
        """
            Retrieves all timer configurations from the Redis database.

            Returns:
               JSONResponse: The response containing all timer configurations.
        """
        conn = ConfigTimer().redis_connection
        conn.select(1)
        keys = conn.keys('*')
        values = conn.mget(keys)
        values = [json.loads(value) for value in values]
        return JSONResponse(
            content={"message": "Successfully retrieve time configuration.", 'data': values, 'code': 200},
            status_code=200)

    @staticmethod
    async def update_time_configuration(data: UpdateConfigTimerSchema):
        """
            Updates an existing timer configuration in the Redis database.

            Args:
                data (UpdateConfigTimerSchema): The updated timer configuration data.

            Returns:
                JSONResponse: The response indicating the result of the operation.
        """
        try:
            if data.notify:
                if not data.message:
                    return APIResponse.error_response("Message field is required.", 400)
                if not data.alert_time:
                    return APIResponse.error_response("Alert time field is required.", 400)

            conn = ConfigTimer().redis_connection
            conn.select(1)
            existing_data = await GetOrSetRedisData().get(conn, data.dict().get('id'))

            if existing_data is None:
                return APIResponse.error_response("No data found", 400)

            new_data = data.dict()
            new_data['duration'] = await TimeFormatConversion().convert_and_format_time(data.duration)
            new_data['alert_time'] = await TimeFormatConversion().convert_and_format_time(data.alert_time)

            await GetOrSetRedisData().set(conn, new_data.get('id'), new_data)
            return APIResponse.success_response(existing_data,
                                                "Successfully update time configuration.", 200)
        except Exception as e:
            return APIResponse.error_response(str(e), 400)
