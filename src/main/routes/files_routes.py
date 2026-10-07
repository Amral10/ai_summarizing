from fastapi import APIRouter, UploadFile, File

files_router = APIRouter(tags=["Arquivos"])

@files_router.post("/files")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size
        }
