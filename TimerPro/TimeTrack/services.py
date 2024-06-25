import json
import uuid

from starlette.responses import JSONResponse

from TimerPro.TimeTrack.schema import ConfigTimerSchema, UpdateConfigTimerSchema, GetTimerSchema
from TimerPro.TimeTrack.utils import GetOrSetRedisData, TimeFormatConversion
from redis_connection import RedisConnection
from response import APIResponse

redis_connection = RedisConnection().redis_client


class ConfigTimer:
    """
        ConfigTimer handles the setting, getting, and updating of timer configurations in a Redis database.
    """

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

            await GetOrSetRedisData().set(redis_connection, new_data.get('id'), new_data)
            return APIResponse.success_response(await GetOrSetRedisData().get(redis_connection, new_data.get('id')),
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
        keys = redis_connection.keys('*')
        values = redis_connection.mget(keys)
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

            existing_data = await GetOrSetRedisData().get(redis_connection, data.dict().get('id'))

            if existing_data is None:
                return APIResponse.error_response("No data found", 400)

            new_data = data.dict()
            new_data['duration'] = await TimeFormatConversion().convert_and_format_time(data.duration)
            new_data['alert_time'] = await TimeFormatConversion().convert_and_format_time(data.alert_time)

            await GetOrSetRedisData().set(redis_connection, new_data.get('id'), new_data)
            return APIResponse.success_response(existing_data,
                                                "Successfully update time configuration.", 200)
        except Exception as e:
            return APIResponse.error_response(str(e), 400)


class GetTimer:
    """
        A class to handle the retrieval of timer information.
    """

    @staticmethod
    async def get_timer(data: GetTimerSchema):
        """
            Retrieve and process timer information based on the provided schema.

            This method converts the duration to a specific format, retrieves configuration data from a Redis store if
            available, and constructs the response accordingly.

            Args:
               data (GetTimerSchema): The schema containing the necessary data to query the timer.

            Returns:
               dict: A dictionary containing the timer information, including any additional configuration data
                     retrieved from Redis.
        """
        data = data.dict()
        data['duration'] = await TimeFormatConversion().convert_and_format_time(data.get('duration'))
        config_data_uuid = data.get('config_data_uuid')
        if config_data_uuid:
            config_data = await GetOrSetRedisData().get(redis_connection, config_data_uuid)
            if config_data is not None and config_data.get('notify'):
                data['message'] = config_data.get('message')
                data['alert_time'] = config_data.get('alert_time')
                data['notify'] = config_data.get('notify')
        return APIResponse.success_response(data,
                                            "Successfully get configuration data for user.", 200)
