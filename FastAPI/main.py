from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel,ValidationError, validator
from typing import Optional, Annotated, List
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import math

app = FastAPI()

@app.get("/")
async def check():
    return {'msg': 'hello'}

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


class PopulationModel(PopulationBase):
    id: int
    date: Optional[str]
    factorial: Optional[int]

    class Config:
        from_attributes=True

    def calculate_factorial(self):
        try:
            factorial = math.factorial(self.count)
        except ValueError:
            return None
        else:
            return factorial
    

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
    if population.count < 0:
        raise HTTPException(status_code=400, detail="Invalid input. 'Count' cannot be a negative number.")
    else:
        db_population = models.Population(count=population.count, date=datetime.now().replace(microsecond=0),factorial=None)
        db.add(db_population)
        db.commit()
        db.refresh(db_population)
        return db_population


@app.get("/population/",response_model=list[PopulationModel])
async def retrive_factorial(db: db_dependency, skip: int=0, limit: int=100):
    population_data = db.query(models.Population).offset(skip).limit(limit).all()
    population_models = []
    for data in population_data:
        population_model = PopulationModel(**data.__dict__)
        population_model.factorial = population_model.calculate_factorial()
        population_models.append(population_model)
    return population_models

