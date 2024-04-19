from database import Base
from sqlalchemy import Column, Integer, String

class Population(Base):
    __tablename__ = "population"

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer)
    date = Column(String)
    factorial = Column(Integer)


