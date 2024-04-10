from fastapi import FastAPI, Path, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()


class Reading(BaseModel):
    number: int
    time: datetime
    #factorial: Optional[int] = None

    
factorial_db = {}

@app.get("/")
def root_endpoint():
    return print('This is the root endpoint.')

@app.get("/get-factorial-by-id/{reading_id}/")
def get_factorial(reading_id:int = Path(..., description="The factorial of a reading you'd like to know.", gt=0, lt=20)):
    return factorial_db[reading_id]

@app.get("/get-factorial-by-reading/{number}")
def get_factorial(number:int = Path(..., description = "The factorial of a reading you'd like to know.", gt=0)):
    for reading_id in factorial_db:
        if factorial_db[reading_id].number == number:
            factorial = factorial_calculation(number)
            return factorial
    raise HTTPException(status_code=404, detail='reading not found')

@app.post("/submit-reading/reading_id/")
def submit_reading(reading_id: int, reading: Reading):
    if reading_id in factorial_db:
        raise HTTPException(status_code=400, detail='reading ID already exists')
    factorial_db[reading_id] = reading
    return factorial_db[reading_id]

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

