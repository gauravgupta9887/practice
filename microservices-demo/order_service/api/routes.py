from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .services import OrderService
from .schemas import OrderCreate, OrderResponse
from .shared.logger import logger

bp = Blueprint("order", __name__, url_prefix="/api/order")

def get_db():
    from .shared.db import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    try:
        data = OrderCreate(**request.json)
        user_id = get_jwt_identity()
        svc = OrderService(next(get_db()))
        order = svc.create(user_id, data)
        return jsonify(order.dict()), 201
    except Exception as e:
        logger.exception("order create error")
        return jsonify({"msg":"server error"}), 500