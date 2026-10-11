from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from src.main.validators.chat_mensage_validator import MensageToAIValidator
from src.main.service.ai_service import chat_bot, chat_bot_with_file

ai_router = APIRouter(tags=["Chat Bot"])

@ai_router.post("/chat", summary="Send message to AI")
async def send_message(msg: MensageToAIValidator):
    dict_body = dict(msg)

    response = chat_bot(dict_body['mensage'])

    return JSONResponse(content={
        "message": "mensagem enviada com sucesso",
        "content": response
    }, status_code=201)


@ai_router.post("/chatWithFile", summary="Send message to AI with file")
async def send_message_with_file(msg: MensageToAIValidator, file: UploadFile = File(...)):
    dict_body = dict(msg)

    response = chat_bot_with_file(dict_body['mensage'], file.file)

    return JSONResponse(content={
        "message": "mensagem enviada com sucesso",
        "content": response
    }, status_code=201)
