from fastapi import APIRouter
from TimerPro.TimeTrack.schema import ConfigTimerSchema, UpdateConfigTimerSchema
from TimerPro.TimeTrack.services import ConfigTimer

router = APIRouter(tags=["Configure Timer"])


@router.post('/set_config-timer', status_code=200)
async def add_config_timer(data: ConfigTimerSchema):
    """
        Add a new timer configuration.

        Args:
            data (ConfigTimerSchema): The timer configuration data to add.

        Returns:
            dict: The result of the operation.
    """
    return await ConfigTimer.set_time_configuration(data)


@router.get('/retrieve-config-timer', status_code=200)
async def config_timer():
    """
        Retrieve the current timer configuration.

        Returns:
            dict: The current timer configuration.
    """
    return await ConfigTimer.get_time_configuration()


@router.put('/update-config-timer', status_code=200)
async def update_config_timer(data: UpdateConfigTimerSchema):
    """
        Update an existing timer configuration.

        Args:
            data (UpdateConfigTimerSchema): The updated timer configuration data.

        Returns:
            dict: The result of the operation.
    """
    return await ConfigTimer.update_time_configuration(data)
