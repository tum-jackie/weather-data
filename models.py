#defining schema for our datatabase
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from pydantic import BaseModel



class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WeatherData(BaseModel):
    latitude : float
    longitude:float
    temperature: float
    humidity: float
    pressure: float

    class Config:
        orm_mode = True