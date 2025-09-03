from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

Characteristics(BaseModel):
    max_speed: float
    max_fuel_capacity: float

class Car(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristics

cars_db: List[Car] = []

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/cars",status_code=201)
def create_car(car: Car):
    cars_db.append(car)
    return car

@app.get("/cars", response_model=List[Car])
def get_cars():
    return cars_db

@app.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: str):
    for car in cars_db:
        if car.identifier == int(car_id):
            return car
    raise HTTPException(status_code=404, detail="The car with the given ID was not found")

@app.put("/cars/{car_id}/characteristics", response_model=Car)
def update_car_characteristics(car_id: str, characteristics: Characteristics):
    for car in cars_db:
        if car.identifier == int(car_id):
            car.characteristics = characteristics
            return car
    raise HTTPException(status_code=404, detail="The car with the given ID was not found")
