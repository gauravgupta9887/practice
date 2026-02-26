from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .services import InventoryService
from .schemas import ProductCreate, ProductResponse
from .shared.logger import logger

bp = Blueprint("inventory", __name__, url_prefix="/api/inventory")

def get_db():
    from .shared.db import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@bp.route("/products", methods=["POST"])
@jwt_required()
def create_product():
    try:
        data = ProductCreate(**request.json)
        svc = InventoryService(next(get_db()))
        prod = svc.add_product(data)
        return jsonify(prod.dict()), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        logger.exception("inventory create error")
        return jsonify({"msg":"server error"}), 500

@bp.route("/products/<int:prod_id>", methods=["GET"])
@jwt_required()
def get_product(prod_id):
    svc = InventoryService(next(get_db()))
    prod = svc.get_product(prod_id)
    if not prod:
        return jsonify({"msg":"not found"}), 404
    return jsonify(prod.dict())