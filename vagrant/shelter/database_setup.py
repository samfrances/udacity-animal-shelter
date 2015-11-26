from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String(80))
    
    def __repr__(self):
        return "<Shelter(id={}, name='{}', city='{}')>".format(self.id, self.name, self.city)
    
class Puppy(Base):
    __tablename__ = 'puppy'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(Enum("male", "female"), nullable = False)
    dateOfBirth = Column(Date)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))
    profile = relationship("PuppyProfile", uselist=False, backref="puppy")
    
    def __repr__(self):
        return "<Puppy(id={}, name='{}', gender='{}')>".format(self.id, self.name, self.gender)

class PuppyProfile(Base):
	__tablename__ = 'puppy_profile'
	
	id = Column(Integer, primary_key=True)
	picture = Column(String)
	description = Column(String(500))
	puppy_id = Column(Integer, ForeignKey('puppy.id'))
	

if __name__ == "__main__":

    engine = create_engine('sqlite:///puppyshelter.db')
 
    Base.metadata.create_all(engine)
