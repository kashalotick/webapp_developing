from typing import Annotated

import pycountry
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator


def validate_country_code(value: str) -> str:
    code = value.strip().upper()

    if not pycountry.countries.get(alpha_2=code):
        raise ValueError(f"Code '{code}' is not valid ISO 3166-1 alpha-2 country code")

    return code

def validate_country_code_or_none(value: str | None) -> str | None:
    if value is None:
        return None
    return validate_country_code(value)

CountryCodeValidator = Annotated[str, BeforeValidator(validate_country_code)]
CountryCodeOrNoneValidator = Annotated[str | None, BeforeValidator(validate_country_code_or_none)]

class DriverCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    country: CountryCodeValidator
    team: str = Field(min_length=1, max_length=255)
    number: int = Field(ge=1, le=99)


class DriverUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=255, default=None)
    country: CountryCodeOrNoneValidator = None
    team: str | None = Field(min_length=1, max_length=255, default=None)
    number: int | None = Field(ge=1, le=99, default=None)


class DriverRead(DriverCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rating: int


class DriverInRace(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_id: int
    race_id: int


class RatingDelta(BaseModel):
    delta: int = Field(ge=-100, le=100)
