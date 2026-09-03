from datetime import time, timedelta, datetime

from pydantic import BaseModel


class DriverCreate(BaseModel):
    name: str
    country: str
    team: str
    number: int


class Driver(DriverCreate):
    id: int
    rating: int


class DriverInRace(BaseModel):
    driver_id: int
    race_id: int


class RaceCreate(BaseModel):
    championship: str
    name: str
    start_date: datetime
    time: timedelta
    track: str


class Race(RaceCreate):
    id: int


class RatingDelta(BaseModel):
    delta: int
class RegisteredDriver(BaseModel):
    driver_id: int
