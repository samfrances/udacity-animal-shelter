from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Enum, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm.session import object_session
from warnings import warn
 
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
    maximum_capacity = Column(Integer, default=10)
    current_occupancy = Column(Integer, default=0)
    
    def __repr__(self):
        return "<Shelter(id={}, name='{}', city='{}')>".format(self.id, self.name, self.city)
    
    def checkIn(self, puppy):
        """Check in a puppy if there is room. (May not be safe from race conditions)"""
        session = object_session(self) #Get current session
        if self.maximum_capacity > self.current_occupancy: # If our shelter is not full
            old_shelter = puppy.shelter # Remember the previous shelter
            puppy.shelter = self # Check the puppy in to this shelter
            # Update the current occupancy of this sheter
            self.current_occupancy = session.query(Puppy).filter(Puppy.shelter == self).count()
            # Update the current occupancy of the previous shelter
            if old_shelter:
                old_shelter.current_occupancy = session.query(Puppy).filter(Puppy.shelter == old_shelter).count()
            session.commit()
        else:
            warn("There is no more room in this shelter")
    
class Puppy(Base):
    __tablename__ = 'puppy'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(Enum("male", "female"), nullable = False)
    dateOfBirth = Column(Date)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter, backref="puppies")
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
