from fastapi import FastAPI
import requests
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import os
import aiohttp
from typing import List
from weather_module import get_lat_long
from models import Weather, WeatherData
from dotenv import load_dotenv
from fastapi import HTTPException, Depends

load_dotenv()
weather_API = os.getenv("weather_key")

app = FastAPI()
weather_endpoint = "https://api.openweathermap.org/data/2.5/weather"


@app.get("/weather/{location}")
async def get_weather(location: str):
    location_coordinates = get_lat_long(location)

    async with aiohttp.ClientSession() as session:
        parameters = {
            "appid": weather_API,
            "lat": location_coordinates[0],
            "lon": location_coordinates[1],
        }
        try:
            response = requests.get(
                url=weather_endpoint, params=parameters
            )  # fetching data from API
            data = await response.json()

            weather_data = WeatherData(
                longitude=data["coord"]["lon"],
                latitude=data["coord"]["lat"],
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                pressure=data["main"]["pressure"],
                description=data["weather"][0]["description"],
            )
            db = SessionLocal()
            db.add(weather_data)
            db.commit()
            db.refresh(weather_data)

            return weather_data
        except:
            raise HTTPException(status_code=404, detail="Location not found")
