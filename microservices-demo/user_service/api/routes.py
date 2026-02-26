from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from .services import UserService
from .schemas import RegisterRequest, LoginRequest, UserResponse
from .shared.logger import logger

bp = Blueprint("user", __name__, url_prefix="/api/users")

def get_db():
    from .shared.db import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@bp.route("/register", methods=["POST"])
def register():
    try:
        data = RegisterRequest(**request.json)
        svc = UserService(next(get_db()))
        user = svc.register(data)
        return jsonify(user.dict()), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        logger.exception("register error")
        return jsonify({"msg": "server error"}), 500

@bp.route("/login", methods=["POST"])
def login():
    try:
        data = LoginRequest(**request.json)
        svc = UserService(next(get_db()))
        token = svc.authenticate(data)
        return jsonify({"access_token": token})
    except ValueError as e:
        return jsonify({"msg": str(e)}), 401
    except Exception as e:
        logger.exception("login error")
        return jsonify({"msg": "server error"}), 500

@bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    svc = UserService(next(get_db()))
    user = svc.db.query(User).filter(User.id == user_id).first()
    return jsonify(UserResponse.from_orm(user).dict())




    

    