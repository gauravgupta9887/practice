from pydantic import BaseModel

class BaseRequest(BaseModel):
    class Config:
        orm_mode = True

class BaseResponse(BaseModel):
    class Config:
        orm_mode = True