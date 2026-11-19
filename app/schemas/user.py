from pydantic import BaseModel


class UserPost(BaseModel):
    login: str
    password: str

class UserRead(BaseModel):
    login: str

class AccessTokenRead(BaseModel):
    token: str