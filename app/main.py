from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.controllers.satellite_controller import router

from app.database.database import Base, engine
import app.models.satellite_model

app = FastAPI(title="Satellite Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/satellite", tags=["Satellite"])

@app.get("/")
def home():
    return {"message": "Satellite Service Running Successfully"}
