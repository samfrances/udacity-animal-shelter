from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Shelter, Puppy, PuppyProfile, Adopter
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()


#Add Shelters
shelter1 = Shelter(name = "Oakland Animal Services", address = "1101 29th Ave", city = "Oakland", state = "California", zipCode = "94601", website = "oaklandanimalservices.org", maximum_capacity=100)
session.add(shelter1)

shelter2 = Shelter(name = "San Francisco SPCA Mission Adoption Center", address="250 Florida St", city="San Francisco", state="California", zipCode = "94103", website = "sfspca.org", maximum_capacity=100)
session.add(shelter2)

shelter3 = Shelter(name = "Wonder Dog Rescue", address= "2926 16th Street", city = "San Francisco", state = "California" , zipCode = "94103", website = "http://wonderdogrescue.org", maximum_capacity=100)
session.add(shelter3)

shelter4 = Shelter(name = "Humane Society of Alameda", address = "PO Box 1571" ,city = "Alameda" ,state = "California", zipCode = "94501", website = "hsalameda.org", maximum_capacity=100)
session.add(shelter4)

shelter5 = Shelter(name = "Palo Alto Humane Society" ,address = "1149 Chestnut St." ,city = "Menlo Park", state = "California" ,zipCode = "94025", website = "paloaltohumane.org", maximum_capacity=100)
session.add(shelter5)

# Add adopters

adopter1 = Adopter(name="Bob")
adopter2 = Adopter(name="Tim")
adopter3 = Adopter(name="Carl")
adopter4 = Adopter(name="Alison")
adopter5 = Adopter(name="Jane")
adopter6 = Adopter(name="Lauren")

adopters = [adopter1, adopter2, adopter3, adopter4, adopter5, adopter6]

#Add Puppies

male_names = ["Bailey", "Max", "Charlie", "Buddy","Rocky","Jake", "Jack", "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley", "Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar", "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley", "Zeus", "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy", "Louie", "Hunter", "Casey", "Rocco", "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo", "Boomer", "Luke", "Henry"]

female_names = ['Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie', 'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger', 'Roxy', 'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess','Emma', 'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia', 'Katie', 'Zoey', 'Madison', 'Stella', 'Penny', 'Belle', 'Casey', 'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine', 'Shelby', 'Sandy', 'Roxie', 'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']

puppy_images = ["http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct", "http://pixabay.com/get/6540c0052781e8d21783/1433170742/dog-280332_1280.jpg?direct","http://pixabay.com/get/8f62ce526ed56cd16e57/1433170768/pug-690566_1280.jpg?direct","http://pixabay.com/get/be6ebb661e44f929e04e/1433170798/pet-423398_1280.jpg?direct","http://pixabay.com/static/uploads/photo/2010/12/13/10/20/beagle-puppy-2681_640.jpg","http://pixabay.com/get/4b1799cb4e3f03684b69/1433170894/dog-589002_1280.jpg?direct","http://pixabay.com/get/3157a0395f9959b7a000/1433170921/puppy-384647_1280.jpg?direct","http://pixabay.com/get/2a11ff73f38324166ac6/1433170950/puppy-742620_1280.jpg?direct","http://pixabay.com/get/7dcd78e779f8110ca876/1433170979/dog-710013_1280.jpg?direct","http://pixabay.com/get/31d494632fa1c64a7225/1433171005/dog-668940_1280.jpg?direct"]

puppy_descriptions = ["A very nice puppy", "A very badly behaved puppy", "A puppy that only a mother could love", "A puppy with rabbies", "Such a cute puppy!"]

#This method will make a random age for each puppy between 0-18 months(approx.) old from the day the algorithm was run.
def CreateRandomAge():
    today = datetime.date.today()
    days_old = randint(0,540)
    birthday = today - datetime.timedelta(days = days_old)
    return birthday

#This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
    return random.uniform(1.0, 40.0)

#This will create a random profile for a Puppy
def CreateRandomProfile():
    picture = random.choice(puppy_images)
    description = random.choice(puppy_descriptions)
    return PuppyProfile(picture=picture, description=description)

#This will check a puppy in to a random shelter
def CheckInToRandomShelter(puppy):
    shelter_id = randint(1,5)
    session.query(Shelter).filter(Shelter.id == shelter_id).one().checkIn(puppy)

# Create puppies and wither have adopted or check in to random shelter
for i,x in enumerate(male_names):
    new_puppy = Puppy(name = x, gender = "male", dateOfBirth = CreateRandomAge(), weight= CreateRandomWeight(),profile=CreateRandomProfile())
    session.add(new_puppy)
    
    if randint(0,1):
        new_puppy.adopt(random.choice(adopters), random.choice(adopters))
    else:
        CheckInToRandomShelter(new_puppy)
    session.commit()

for i,x in enumerate(female_names):
    new_puppy = Puppy(name = x, gender = "female", dateOfBirth = CreateRandomAge(), weight= CreateRandomWeight(),profile=CreateRandomProfile())
    session.add(new_puppy)
    
    if randint(0,1):
        new_puppy.adopt(random.choice(adopters), random.choice(adopters))
    else:
        CheckInToRandomShelter(new_puppy)
    session.commit()

# Create an unoccupied shelter

shelter6 = Shelter(name = "Very Small Shelter" ,address = "1444 Chestnut St." ,city = "Menlo Park", state = "California" ,zipCode = "94025", website = "verysmallanimalshelter.org", maximum_capacity=3)
session.add(shelter6)
session.commit()
