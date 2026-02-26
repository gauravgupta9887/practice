from sqlalchemy.orm import Session
from .models import Product
from .schemas import ProductCreate, ProductResponse
from .shared.logger import logger

class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def add_product(self, data: ProductCreate) -> ProductResponse:
        if self.db.query(Product).filter(Product.name == data.name).first():
            raise ValueError("Product already exists")
        prod = Product(**data.dict())
        self.db.add(prod)
        self.db.commit()
        self.db.refresh(prod)
        logger.info(f"Product {prod.id} added")
        return ProductResponse.from_orm(prod)

    def get_product(self, prod_id: int) -> ProductResponse | None:
        prod = self.db.query(Product).filter(Product.id == prod_id).first()
        return ProductResponse.from_orm(prod) if prod else None