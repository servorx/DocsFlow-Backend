from fastapi import FastAPI, Depends
from app.routes.data_upload import upload_router
from app.routes.sesion import sesion
from app.routes.user.users import router as user_router
from app.auth.dependencias import get_current_user

app = FastAPI(
    title="API Proyecto",
    version="1.0.0"
)

# Routers
app.include_router(upload_router)
app.include_router(sesion.router, tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])

# Health check
@app.get("/", dependencies=[Depends(get_current_user)])
def health_check():
    return {"status": "ok"}
