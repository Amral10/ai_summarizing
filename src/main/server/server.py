from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.main.routes.users_routes import users_router
from src.main.routes.files_routes import files_router
from src.main.routes.ai_routes import ai_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(users_router)
app.include_router(files_router)
app.include_router(ai_router)
