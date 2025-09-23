from fastapi import FastAPI, APIRouter
from app.routes.data_upload import upload_router

app = FastAPI()
app.include_router(upload_router)

