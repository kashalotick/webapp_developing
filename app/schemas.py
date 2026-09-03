from datetime import time, timedelta, datetime

from pydantic import BaseModel


class DriverCreate(BaseModel):
    name: str
    country: str
    team: str
    number: int


class DriverUpdate(BaseModel):
    name: str | None = None
    country: str | None = None
    team: str | None = None
    number: int | None = None

class Driver(DriverCreate):
    id: int = 0
    rating: int = 0


class DriverInRace(BaseModel):
    id: int = 0
    driver_id: int
    race_id: int


class RaceCreate(BaseModel):
    championship: str
    name: str
    start_date: datetime
    time: timedelta
    track: str

class RaceUpdate(BaseModel):
    championship: str | None = None
    name: str | None = None
    start_date: datetime | None = None
    time: timedelta | None = None
    track: str | None = None


class Race(RaceCreate):
    id: int = 0


class RatingDelta(BaseModel):
    delta: int
class DriverRegistration(BaseModel):
    driver_id: int
