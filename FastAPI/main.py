from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Annotated
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import math
import models


app = FastAPI()

#allow localhost 3000 to call api
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
    #factorial: Optional[int]
    factorial: Optional[str]

    class Config:
        orm_mode=True

    def calculate_factorial(self):
        try:
            if 0 <= self.count < 170:
                factorial = math.factorial(self.count)
                return factorial
            elif self.count >= 170:
                return "Infinity"
        except ValueError:
            return None
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#create dependency 
db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

#root
@app.get("/")
async def check():
    return {'msg': 'hello'}

#endpoint for submission
@app.post("/population/", response_model=PopulationModel,tags=["Submit"])
async def create_population(population:PopulationBase, db:db_dependency):
    if population.count < 0:
        raise HTTPException(status_code=400, detail="Invalid input. 'Count' cannot be a negative number.")
    else:
        db_population = models.Population(count=population.count, date=datetime.now().replace(microsecond=0),factorial=None)
        db.add(db_population)
        db.commit()
        db.refresh(db_population)
        return db_population

#endpoint for retrieval 
@app.get("/population/",response_model=list[PopulationModel],tags=["Retrieve"])
async def retrive_factorial(db: db_dependency, skip: int=0, limit: int=100):
    population_data = db.query(models.Population).offset(skip).limit(limit).all()

    #calculate and add factorials to database
    population_models = []
    for data in population_data:
        population_model = PopulationModel(**data.__dict__)
        population_model.factorial = population_model.calculate_factorial()
        population_models.append(population_model)
    return population_models

#endpoint for search
@app.get("/population/search/", response_model=list[PopulationModel], tags=["Search"])
async def search_population_by_count(
    db: db_dependency,
    count: Optional[int] = Query(None, description="Search by count")
):
    if count < 0:
        raise HTTPException(status_code=400, detail="Invalid input. Count cannot be a negative number.")
    query = db.query(models.Population)

    #add filter conditions if count is provided
    if count is not None:
        query = query.filter(models.Population.count == count)

    population_data = query.all()

    #check if population_data is empty
    if not population_data:
        raise HTTPException(status_code=404, detail="Count not found in the database.")

    population_models = []
    for data in population_data:
        population_model = PopulationModel(**data.__dict__)
        population_model.factorial = population_model.calculate_factorial()
        population_models.append(population_model)
    
    return population_models





