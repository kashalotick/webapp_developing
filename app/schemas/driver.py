from datetime import time, timedelta, datetime
from typing import Annotated

import pycountry
from pydantic import BaseModel, ConfigDict, field_validator, Field, BeforeValidator


def validate_country_code(value: str) -> str:
    code = value.strip().upper()

    if not pycountry.countries.get(alpha_2=code):
        raise ValueError(f"Code '{code}' is not valid ISO 3166-1 alpha-2 country code")

    return code

CountryCodeValidator = Annotated[str, BeforeValidator(validate_country_code)]

class DriverCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    country: CountryCodeValidator
    team: str = Field(min_length=1, max_length=255)
    number: int = Field(ge=1, le=99)


class DriverUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=255, default=None)
    country: CountryCodeValidator | None = None
    team: str | None = Field(min_length=1, max_length=255, default=None)
    number: int | None = Field(ge=1, le=99, default=None)


class DriverRead(DriverCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int = 0
    rating: int = 0


class DriverInRace(BaseModel):
    id: int = 0
    driver_id: int
    race_id: int


class RatingDelta(BaseModel):
    delta: int
