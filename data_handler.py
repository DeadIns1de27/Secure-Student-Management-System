'''
Storage Layer:

sqlalchemy used to store data objects in 
a serverless data base (sqlite) titled database.db

-add load record function
-add update record function
-add delete record function
'''

#Import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base

#Import Data Layer
from student import StudentRecord

#Creates database class
Base = declarative_base()

#Creates sqlite database
engine = sa.create_engine("sqlite:///database.db")

#Makes a session
Session = sessionmaker(bind= engine)

#Creates table for student records
class StudentTable(Base):

    #Table name
    __tablename__ = "student_info"

    #Columns
    studentID = sa.Column(sa.Integer, unique = True, primary_key = True)
    name = sa.Column(sa.String)
    age = sa.Column(sa.Integer)
    gender = sa.Column(sa.String)
    phone = sa.Column(sa.String)
    grade = sa.Column(sa.Text)

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