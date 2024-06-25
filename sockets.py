import socketio
from TimerPro.TimeTrack.utils import GetOrSetRedisData
from redis_connection import RedisConnection

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
socket_app = socketio.ASGIApp(socketio_server=sio)


@sio.event
async def connect(sid, env):
    """
        Handles the event when a new client connects.

        Args:
            sid (str): The session ID of the connected client.
            env: The environment data associated with the connection.
    """
    print("New Client Connected to This id :" + " " + str(sid))


@sio.event
async def set_timer(sid, data):
    """
        Handles the 'set_timer' event from clients to set a timer.

        Args:
            sid (str): The session ID of the client.
            data (dict): The data containing timer information.

        Emits:
            'get_timer' event: Emits the updated timer data to clients.
    """
    try:
        redis_connection = RedisConnection().redis_client
        redis_connection.select(0)
        await GetOrSetRedisData().set(redis_connection, data.get('id'), data)
        data = await GetOrSetRedisData().get(redis_connection, data.get('id'))
        config_data_uuid = data.get('config_data_uuid')
        if config_data_uuid:
            redis_connection.select(1)
            config_data = await GetOrSetRedisData().get(redis_connection, config_data_uuid)
            if config_data is not None and config_data.get('notify'):
                data['message'] = config_data.get('message')
                data['alert_time'] = config_data.get('alert_time')
                data['notify'] = config_data.get('notify')
        await sio.emit(event='get_timer', data=data)
    except Exception as e:
        await sio.emit(event='get_timer', data=str(e))


@sio.event
async def delete_time_data(sid, data):
    """
        Handle deletion of data from Redis based on provided 'id'.

        Args:
            sid (str): Session ID of the socket connection.
            data (dict): Dictionary containing the 'id' key to identify the data in Redis.

        Returns:
            None

        Raises:
            socketio.exceptions.SocketIOError: If there is an error during the deletion process.
    """
    try:
        redis_connection = RedisConnection().redis_client
        redis_connection.select(0)
        existing_data = await GetOrSetRedisData().get(redis_connection, data.get('id'))
        if existing_data is not None:
            redis_connection.delete(data.get('id'))
    except Exception as e:
        await sio.emit(event='disconnect', data=str(e))


@sio.event
async def disconnect(sid):
    """
        Handles the event when a client disconnects.

        Args:
            sid (str): The session ID of the disconnected client.
    """
    print("Client Disconnected: " + " " + str(sid))
