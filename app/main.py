from fastapi import FastAPI
from app.routes.data_upload import upload_router
from app.routes.sesion import sesion 

app = FastAPI(
    title="API Proyecto",
    version="1.0.0"
)

# Routers
app.include_router(upload_router)
app.include_router(sesion.router, prefix="/auth", tags=["Auth"]) 

# Health check
@app.get("/")
def health_check():
    return {"status": "ok"}
