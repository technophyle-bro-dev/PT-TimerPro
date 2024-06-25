from datetime import time
from typing import Optional
from pydantic import BaseModel


class ConfigTimerSchema(BaseModel):
    """
        Schema for configuring a timer.

        Attributes:
           name (str): The name of the timer.
           duration (time): The duration of the timer.
           notify (bool): Whether to notify when the timer ends.
           alert_time (Optional[time]): The time to alert.
           message (Optional[str]): The message to display when alerting.
    """
    name: str
    duration: time
    notify: bool
    alert_time: Optional[time] = None
    message: Optional[str] = None


class UpdateConfigTimerSchema(BaseModel):
    """
        Schema for updating an existing timer configuration.

        Attributes:
           id (str): The unique identifier of the timer configuration.
           name (str): The name of the timer.
           duration (time): The duration of the timer.
           notify (bool): Whether to notify when the timer ends.
           alert_time (Optional[time]): The time to alert.
           message (Optional[str]): The message to display when alerting.
    """
    id: str
    name: str
    duration: time
    notify: bool
    alert_time: Optional[time] = None
    message: Optional[str] = None


class GetTimerSchema(BaseModel):
    """
        Schema for the timer data required to retrieve timer information.

        Attributes:
            id (str): The unique identifier for the timer.
            name (str): The name of the timer.
            config_data_uuid (str): The unique identifier for the configuration data associated with the timer.
            duration (time): The duration of the timer.
    """
    id: str
    name: str
    config_data_uuid: str
    duration: time

