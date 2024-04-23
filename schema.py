import pydantic
import typing

class CreateAd(pydantic.BaseModel):
    name: str
    password: str


    @pydantic.validator('password')
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError(f'Minimal length of password is 8')
        return v

class UpdateAd(pydantic.BaseModel):
    description: typing.Optional[str]
    name: typing.Optional[str]
    owner: str

    @pydantic.validator('description')
    def check_desc_len(cls, v):
        if len(v) < 10:
            raise ValueError(f'Minimal length of description is 10')
        return v