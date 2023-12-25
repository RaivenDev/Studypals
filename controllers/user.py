from datetime import datetime

from factory import api, db
from flask import Blueprint, jsonify
from flask.globals import request
from models.user import User, UserCreate
from spectree import Response

import json

from models.user import UserResponse
from models.user import UserResponseList
from models.user import UserEdit
from utils.responses import DefaultResponse



from flask_jwt_extended import jwt_required, current_user

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")


@user_controller.get("/", methods=["GET"])
@api.validate(resp=Response(HTTP_200=UserResponseList), tags=["users"])
@jwt_required()
def get_users():
    """
    Get all users
    """

    if not (current_user and current_user.role.can_manage_users):
        return {"msg": "You don't have permission to view all users."}, 403

    users = User.query.all()

    response = UserResponseList(
        __root__ = [UserResponse.from_orm(user).dict() for user in users]
    ).json()

    return jsonify(json.loads(response)), 200


@user_controller.get("/<int:user_id>")
@api.validate(resp=Response(HTTP_200=UserResponse, HTTP_404=DefaultResponse), tags=["users"])
def get_user(user_id):
    """
    Get a specified user
    """

    if not (current_user and current_user.role.can_access_sensitive_information):
        return {
            "msg": "You don't have permission to access this user information."
        }, 403
    
    user = User.query.get(user_id)

    if user is None:
        return {"msg": f"There is no user with id {user_id}"}, 404

    response = UserResponse.from_orm(user).json()

    return json.loads(response), 200


@user_controller.post("/")
@api.validate(
    json=UserCreate,
    resp=Response(HTTP_201=DefaultResponse),
    security={},
    tags=["users"],
)
def post_user():
    """
    Create an user
    """
    data = request.json

    if User.query.filter_by(username=data["username"]).first():
        return {"msg": "username not avaiable"}, 409

    if "birthdate" in data:
        if data["birthdate"].endswith("Z"):
            data["birthdate"] = data["birthdate"][:-1]

    user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        country=data["country"],
        birthdate=datetime.fromisoformat(data["birthdate"])
        if "birthdate" in data
        else None,
    )

    db.session.add(user)
    db.session.commit()

    return {"msg": "User created successfully."}, 201


@user_controller.put("/")
@api.validate(json=UserEdit, resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse), tags=["users"])
@jwt_required()
def put_user(user_id):
    """
    Update an user
    """
    user = current_user

    data = request.json

    if "birthdate" in data:
        if data["birthdate"].endswith("Z"):
            data["birthdate"] = data["birthdate"][:-1]
        user.birthdate = datetime.fromisoformat(data["birthdate"])

    user.username = data["username"]
    user.email = data["email"]
    user.country = data["country"]

    db.session.commit()

    return {"msg": "User was updated."}, 200


@user_controller.delete("/<int:user_id>", methods=["DELETE"])
@api.validate(resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse), tags=["users"])
@jwt_required()
def delete_user(user_id):
    """
    Delete an user
    """

    if not (current_user and current_user.role.can_manage_users):
        return {"msg": "You don't have permission to delete this user."}, 403

    user = User.query.get(current_user.id)

    db.session.delete(user)
    db.session.commit()

    return {"msg": "User deleted from the database."}, 200


@user_controller.route("/me", methods=["GET"])
@api.validate(resp=Response(HTTP_200=UserResponse), tags=["users"])
@jwt_required()
def me():
    """Returns information about the current user"""

    response = UserResponse.from_orm(current_user).json()

    return json.loads(response), 200