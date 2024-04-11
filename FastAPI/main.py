from fastapi import FastAPI, Path, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, Annotated, List
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

@app.get("/")
async def check():
    return 'hello'

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers = ["*"]
)

class PopulationBase(BaseModel):
    count: int
    date: str

class PopulationModel(PopulationBase):
    id: int

    class Config:
        from_attributes=True

# class FactorialBase(BaseModel):
#     number: int
#     factorial: int

# class FactorialModel(FactorialBase):
#     id: int

#     class Config:
#         orm_mode=True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
models.Base.metadata.create_all(bind=engine)


@app.post("/population/", response_model=PopulationModel)
async def create_population(population:PopulationBase, db:db_dependency):
    db_population = models.Population(**population.model_dump())
    db.add(db_population)
    db.commit()
    db.refresh(db_population)
    return db_population


@app.get("/retrive/",response_model=list[PopulationModel])
async def retrive_factorial(db: db_dependency, skip: int=0, limit: int=100):
    factorial = db.query(models.Population).offset(skip).limit(limit).all()
    return factorial


def factorial_calculation(num):
    factorial = 1
    if num < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif num == 0:
        factorial = 1 
    else:
        for i in range(1, num):
            factorial *= i
        return factorial

