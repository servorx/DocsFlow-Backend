from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from typing import List, Optional
from ..auth.dependencias import get_current_user
from ..core.database import get_session
from ..models.extrated_data import ExtratedData
from ..models.key_data import KeyData

document_router = APIRouter()


# ✅ 1️⃣ Obtener todos los documentos (tablas extraídas)
@document_router.get("/", response_model=List[ExtratedData])
def get_all_documents(
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    department_id = user["department_id"]
    documents = session.exec(
        select(ExtratedData).where(ExtratedData.department_id == department_id)
    ).all()

    if not documents:
        raise HTTPException(status_code=404, detail="No se encontraron documentos.")
    
    return documents


# ✅ 2️⃣ Obtener un documento por su ID
@document_router.get("/{id_table}", response_model=ExtratedData)
def get_document_by_id(
    id_table: int,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    document = session.get(ExtratedData, id_table)
    if not document or document.department_id != user["department_id"]:
        raise HTTPException(status_code=404, detail="Documento no encontrado o no autorizado.")
    return document


# ✅ 3️⃣ Obtener todas las tablas (key-values) asociadas a un documento
@document_router.get("/tables/{document_id}", response_model=List[KeyData])
def get_tables_by_document_id(
    document_id: int,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    document = session.get(ExtratedData, document_id)
    if not document or document.department_id != user["department_id"]:
        raise HTTPException(status_code=403, detail="No autorizado para ver este documento.")
    
    tables = session.exec(
        select(KeyData).where(KeyData.table_id == document_id)
    ).all()
    
    if not tables:
        raise HTTPException(status_code=404, detail="No hay tablas asociadas a este documento.")
    
    return tables


# ✅ 4️⃣ Buscar datos clave (KeyData) por palabra clave
@document_router.get("/tables/search", response_model=List[KeyData])
def search_key_data(
    q: Optional[str] = Query(None, description="Texto de búsqueda en 'key' o 'value'"),
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    if not q:
        raise HTTPException(status_code=400, detail="Debe proporcionar un parámetro de búsqueda (q).")

    results = session.exec(
        select(KeyData)
        .where(KeyData.department_id == user["department_id"])
        .where(
            (KeyData.key.ilike(f"%{q}%")) | 
            (KeyData.value.ilike(f"%{q}%"))
        )
    ).all()

    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron coincidencias.")
    
    return results


# ✅ 5️⃣ Eliminar un documento y sus datos asociados
@document_router.delete("/{id_table}")
def delete_document(
    id_table: int,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    document = session.get(ExtratedData, id_table)
    if not document or document.department_id != user["department_id"]:
        raise HTTPException(status_code=404, detail="Documento no encontrado o no autorizado.")

    # Borrar las key_data relacionadas primero (para mantener integridad)
    session.exec(
        select(KeyData).where(KeyData.table_id == id_table)
    ).all()
    session.query(KeyData).filter(KeyData.table_id == id_table).delete()

    # Luego eliminar el documento
    session.delete(document)
    session.commit()

    return JSONResponse(
        content={"message": f"Documento con ID {id_table} eliminado correctamente."},
        status_code=200
    )
