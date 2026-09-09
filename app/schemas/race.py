from datetime import timedelta, datetime

from pydantic import BaseModel, ConfigDict, Field


class RaceCreate(BaseModel):
    championship: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=255)
    start_date: datetime
    time: timedelta = Field(ge=timedelta(seconds=0))
    track: str = Field(min_length=1, max_length=255)


class RaceUpdate(BaseModel):
    championship: str | None = Field(min_length=1, max_length=255, default=None)
    name: str | None = Field(min_length=1, max_length=255, default=None)
    start_date: datetime | None = None
    time: timedelta | None = Field(ge=timedelta(seconds=0), default=None)
    track: str | None = Field(min_length=1, max_length=255, default=None)


class RaceRead(RaceCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int = 0


class DriverRegistration(BaseModel):
    driver_id: int
