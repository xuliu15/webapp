from fastapi import FastAPI, Path, HTTPException, status, Depends
from pydantic import BaseModel, Field
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
    
class PopulationModel(PopulationBase):
    id: int
    #date: Optional[datetime] 
    date: Optional[datetime] = Field(default_factory=datetime.now)
    # date: Optional[str] 
    factorial: Optional[int]

    class Config:
        from_attributes=True

    def calculate_factorial(self):
        factorial = 1
        for i in range(1, self.count + 1):
            factorial *= i
        return factorial
    
    def get_datetime(self):
        return self.date


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
    #db_population = models.Population(**population.model_dump())
    db_population = models.Population(count=population.count, date=datetime.now().replace(microsecond=0), factorial=None)
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
        #population_model.date = population_model.get_datetime()
        population_models.append(population_model)
    return population_models

