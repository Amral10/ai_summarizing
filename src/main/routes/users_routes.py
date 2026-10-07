from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.main.validators.user_register_validator import UserRegisterValidator

users_router = APIRouter(tags=["Usuários"])



@users_router.post("/users")
async def create_user(body: UserRegisterValidator):
    dict_body = dict(body)

    return JSONResponse(content={
        "message": "Usuário criado com sucesso",
        "content": dict_body
    }, status_code=201)
