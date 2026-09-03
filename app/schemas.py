from datetime import time, timedelta, datetime

from pydantic import BaseModel


class Driver(BaseModel):
    id: int
    name: str
    country: str
    team: str
    number: int
    rating: int


class DriverInRace(BaseModel):
    driver_id: int
    race_id: int

class Race(BaseModel):
    id: int
    championship: str
    name: str
    start_date: datetime
    time: timedelta
    track: str
