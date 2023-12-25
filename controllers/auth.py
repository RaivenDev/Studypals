# Validação da rota
from factory import api
from pydantic import BaseModel
from spectree import Response

# Blueprint e acesso aos dados da requisição
from flask import Blueprint, request

# Função para criar JWT token
from flask_jwt_extended import create_access_token

# Modelo para buscarmos o usuário no banco de dados
from models import User

# Esquema com retorno de um campo "msg"
from utils.responses import DefaultResponse

from flask_jwt_extended import jwt_required

auth_controller = Blueprint("auth_controller", __name__, url_prefix="/auth")

# Recebimento de informações de login
class LoginMessage(BaseModel):
    username: str
    password: str

# Retorno do Token de acesso
class LoginResponseMessage(BaseModel):
    access_token: str

@auth_controller.post("/login")
@api.validate(
    json=LoginMessage,
    resp=Response(HTTP_200=LoginResponseMessage, HTTP_401=DefaultResponse),
    security={},
    tags=["auth"],
)
def login():
    """Login in the system"""

    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    if user and user.verify_password(data["password"]):
        return {
            "access_token": create_access_token(
                identity=user.username, expires_delta=None
            )
        }

    return {"msg": "Username and password do not match."}, 401

@auth_controller.post("/logout")
@api.validate(resp=Response(HTTP_200=DefaultResponse), tags=["auth"])
@jwt_required()
def logout():
    """Logout user"""
    return {"msg": "Logout successfully."}