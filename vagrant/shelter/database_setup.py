from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Enum, Table
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
    adopters = relationship("Adopter", secondary=(lambda: puppy_adopter), backref="puppies")
    
    def __repr__(self):
        return "<Puppy(id={}, name='{}', gender='{}')>".format(self.id, self.name, self.gender)

class PuppyProfile(Base):
	__tablename__ = 'puppy_profile'
	
	id = Column(Integer, primary_key=True)
	picture = Column(String)
	description = Column(String(500))
	puppy_id = Column(Integer, ForeignKey('puppy.id'))

class Adopter(Base):
	__tablename__ = 'adopter'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	
	def __repr__(self):
		return "<Adopter(id={}, name='{}')>".format(self.id, self.name)
	
# Association table between adopters and puppies
puppy_adopter = Table('puppy_adopter', Base.metadata,
    Column('puppy_id', Integer, ForeignKey('puppy.id')),
    Column('adopter_id', Integer, ForeignKey('adopter.id'))
)

if __name__ == "__main__":

    engine = create_engine('sqlite:///puppyshelter.db')
 
    Base.metadata.create_all(engine)
