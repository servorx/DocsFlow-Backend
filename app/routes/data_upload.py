from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import shutil
import uuid
from ..auth.dependencias import get_current_user

upload_router = APIRouter()


@upload_router.post("/upload/")
async def upload_file(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    if not file:
        raise HTTPException(status_code=400, detail="No se ha proporcionado ningún archivo")
    
    # Validar que el archivo tenga nombre
    if not file.filename:
        raise HTTPException(status_code=400, detail="El archivo debe tener un nombre válido")
    
    # Validar tipo de archivo (solo PDFs por defecto)
    allowed_extensions = ['.pdf']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    # Generar nombre único para evitar sobrescrituras
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    
    return JSONResponse(content={
        "message": "Archivo subido exitosamente",
        "filename": file.filename,
        "saved_as": unique_filename,
        "type": file.content_type
    })
