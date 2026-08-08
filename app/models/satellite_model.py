import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from app.database.database import Base


class SatelliteImage(Base):

    __tablename__ = "satellite_images"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    filename = Column(String, nullable=False)

    satellite = Column(String, nullable=False)

    capture_time = Column(DateTime)

    latitude = Column(Float)

    longitude = Column(Float)

    resolution = Column(Float)

    cloud_cover = Column(Float)

    processed = Column(Boolean, default=False)

    image_path = Column(String)
    hazard = Column(String)
    severity = Column(String)
    confidence = Column(Float)
