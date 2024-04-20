from database import Base
from sqlalchemy import Column, Integer, String

#Create table for sqldatabase
class Population(Base):
    __tablename__ = "population"
    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer)
    date = Column(String)
    factorial = Column(Integer)


