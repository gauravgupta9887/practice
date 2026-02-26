from sqlalchemy.orm import Session
from .models import Order
from .schemas import OrderCreate, OrderResponse
from .shared.db import SessionLocal
from .shared.logger import logger

class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, data: OrderCreate) -> OrderResponse:
        # simple validation – no stock check for brevity
        order = Order(user_id=user_id,
                      product_id=data.product_id,
                      quantity=data.quantity,
                      total=data.quantity*float(data.quantity))
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        logger.info(f"Order {order.id} created")
        return OrderResponse.from_orm(order)