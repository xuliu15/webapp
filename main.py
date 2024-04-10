from fastapi import FastAPI, Path, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()


factorial_db = {}

@app.get("/")
def root_endpoint():
    return print('This is the root endpoint.')
#Should this endpoint retrive only 1 each time or all readings each time? database needed for latter case?
@app.get("/get-factorial/{number}")
def get_factorial(number:int = Path(..., description = "The factorial of a reading you'd like to retrive.", gt=0)):
    factorial = factorial_calculation(number)
    return {"Factorial": factorial}
#Should have both{number}${datetime}?
@app.post("/submit-reading/{number}")
def submit_reading(timestamp:str, number: int = Path(..., description = "The number should be a integer.", gt=0)):
 #maybe should validate timestamp here?
    factorial_db[number] = timestamp
    return {"timestamp": timestamp, "Integer":number}

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

