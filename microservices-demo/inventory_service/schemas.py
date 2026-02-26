from .shared.schemas.base import BaseRequest, BaseResponse
from pydantic import Decimal, PositiveInt, constr

class ProductCreate(BaseRequest):
    name: constr(min_length=1)
    description: str | None = None
    price: Decimal
    quantity: PositiveInt

class ProductResponse(BaseResponse):
    id: int
    name: str
    description: str | None
    price: Decimal
    quantity: int