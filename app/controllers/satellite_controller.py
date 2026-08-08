from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil

from app.database.dependencies import get_db
from app.models.satellite_model import SatelliteImage

router = APIRouter()


@router.get("/")
def test():
    return {
        "status": "Satellite Controller Working"
    }


@router.get("/images")
def get_images(db: Session = Depends(get_db)):
    images = db.query(SatelliteImage).all()
    return images


@router.post("/upload")
def upload_image(
    file: UploadFile = File(...),
    satellite: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    resolution: float = Form(...),
    cloud_cover: float = Form(...),
    db: Session = Depends(get_db)
):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = SatelliteImage(
        filename=file.filename,
        satellite=satellite,
        capture_time=datetime.utcnow(),
        latitude=latitude,
        longitude=longitude,
        resolution=resolution,
        cloud_cover=cloud_cover,
        processed=False,
        image_path=file_path
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return {
        "message": "Image Uploaded Successfully",
        "id": image.id
    }


@router.post("/analyze/{image_id}")
def analyze_image(
    image_id: str,
    db: Session = Depends(get_db)
):
    image = db.query(SatelliteImage).filter(
        SatelliteImage.id == image_id
    ).first()

    if image is None:
        return {
            "message": "Image not found"
        }

    # Demo AI Analysis
    image.hazard = "Flood"
    image.severity = "High"
    image.confidence = 94.5
    image.processed = True

    db.commit()
    db.refresh(image)

    return {
        "id": image.id,
        "filename": image.filename,
        "hazard": image.hazard,
        "severity": image.severity,
        "confidence": image.confidence,
        "processed": image.processed
    }
