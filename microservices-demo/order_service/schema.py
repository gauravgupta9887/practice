from .shared.schemas.base import BaseRequest, BaseResponse
from pydantic import PositiveInt, Decimal

class OrderCreate(BaseRequest):
    product_id: int
    quantity: PositiveInt

class OrderResponse(BaseResponse):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total: Decimal