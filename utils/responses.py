from pydantic import BaseModel


class DefaultResponse(BaseModel):
    msg: str

class OrmBase(BaseModel):
    id: int

    class Config:
        orm_mode = True