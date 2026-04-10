'''
Storage Layer:

sqlalchemy used to store data objects in 
a serverless data base (sqlite) titled database.db

-add GradeManager table
-add load record function
-add update record function
-add delete record function
'''

#Import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base

#Import Data Layer
from student import StudentRecord

#Creates database class
Base = declarative_base()

#Creates sqlite database
engine = create_engine("sqlite:///database.db")

#Makes a session
Session = sessionmaker(bind= engine)

#Creates table for student records
class StudentTable(Base):

    #Table name
    __tablename__ = "student_info"

    #Columns
    id = Column(Integer, primary_key = True, autoincrement = True)
    studentID = Column(Integer, unique = true)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    phone = Column(String)

#Creates tables
Base.metadata.create_all(engine)

#Saves student records to database
def save_student(record):
    session = Session()

    studentRow = StudentTable(studentID = record.studentID,
                              name = record.name,
                              age = record.age,
                              gender = record.gender,
                              phone = record.phoneNumber)
    
    #Adds and commits new row to database
    session.add(studentRow)
    session.commit()
    session.close()