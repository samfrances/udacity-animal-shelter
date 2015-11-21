import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, Float

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = "shelter"
    
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    address = Column(String(80))
    city = Column(String(80))
    state = Column(String(80))
    zipcode = Column(String(80))
    website = Column(String(80))
    
class Puppy(Base):
    __tablename__ = "puppy"
    
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    dob = Column(Date)
    gender = Column(Enum("male", "female"))
    weight = Column(Float)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    
    shelter = relationship(Shelter)

if __name__ == "__main__":

    engine = create_engine('sqlite:///shelter.db', echo=True)

    Base.metadata.create_all(engine)
