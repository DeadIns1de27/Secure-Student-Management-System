'''
Storage Layer:

sqlalchemy used to store data objects in 
a serverless data base (sqlite) titled database.db

-add save_password
-add load_password
-add update_password
-add admin column to studentTable
'''

#Import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

#Import Data Layer
from student import StudentRecord

#Import security Layer
from security import hash_password

#Sets databases file location
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

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

#Stores studentID and hased password
class StudentCredentials(Base):

    #Table name
    __tablename__ = "student_creds"

    #Columns
    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    studentID = sa.Column(sa.Integer, sa.ForeignKey("student_info.studentID"))
    password = sa.Column(sa.String)


#Creates tables
Base.metadata.create_all(engine)

#Saves student records to database
def save_student(record) -> None:
    session = Session()

    try:
        studentRow = StudentTable(studentID = record.studentID,
                                name = record.name,
                                age = record.age,
                                gender = record.gender,
                                phone = record.phoneNumber,
                                grade = record.grade)
    
        #Adds and commits new row to database
        session.add(studentRow)
        session.commit()

    #Raises exeception if student id already in use
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Student ID {record.studentID} already in use.")

    finally:
        session.close()

#Loads student record from data base using studentID
def load_student(student_id: int) -> dict | None:
    session = Session()

    try:
        #Finds the student record with specified studentID
        student = sa.select(StudentTable).where(StudentTable.studentID == student_id)
        row = session.execute(student).scalar_one_or_none()

        if row is None:
            return None
    
        #Returns specified student record
        return {c.name: getattr(row, c.name) for c in row.__table__.columns}

    finally:
        session.close()

#Update student record
def update_student(student_id, **updates):
    session = Session()

    try:
        #Finds the student record with specified studentID    
        student = sa.select(StudentTable).where(StudentTable.studentID == student_id)
        row = session.execute(student).scalar_one_or_none()

        #Checks if row is empty
        if row is None:
            return {"succes": False, "error": "Student not found"}
        
        #all valid fields in the table
        validFields = StudentTable.__table__.columns.keys()

        #interate through specifeid row
        for key, value in updates.items():
            #Checks if key is a valid field
            if key not in validFields:
                return {"success": False, "error": f"Invalid field: {key}"}
            #Updates specifeid values
            setattr(row, key, value)
            
        session.commit()
        return {"success": True, "message": "Student updated successfully"}
    
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    
    finally:
        session.close()

#Delete a row from database
def delete_student(student_id):
    session = Session()

    #Finds the student record with specified studentID    
    try:
        student = sa.select(StudentTable).where(StudentTable.studentID == student_id)
        row = session.execute(student).scalar_one_or_none()

        #Checks if student exists
        if row is None:
            return {"succes": False, "error": "Student not found"}
        
        #deletes specified row
        session.delete(row)
        session.commit()
        return {"success": True, "message": "Student deleted successfully"}
    
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    
    finally:
        session.close()

#Saves password to database
def save_password(current_ID: int, hashed_password: str) -> None:
    session = Session()

    try:

        #Adds and commits new row to database
        session.add(StudentCredentials(studentID = current_ID, password = hashed_password))
        session.commit()

    #Raises exeception if student id already in use
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Student ID {current_ID} already in use.")

    finally:
        session.close()

#Loads password from data base using studentID
def load_password(student_id: int) -> dict | None:
    session = Session()

    try:
        #Finds the password accosiated with specified studentID
        query = sa.select(StudentCredentials.password).where(StudentCredentials.studentID == student_id)
        password = session.execute(query).scalar_one_or_none()

    
        #Returns specified password
        return password

    finally:
        session.close()

#Update password
def update_password(student_id, new_password):
    session = Session()

    try:
        #Finds the student record with specified studentID    
        query = sa.select(StudentCredentials).where(StudentCredentials.studentID == student_id)
        row = session.execute(query).scalar_one_or_none()

        #Checks if row is empty
        if row is None:
            return {"succes": False, "error": "Student not found"}

        
        #Updates specifeid values
        row.password = new_password
            
        session.commit()
        return {"success": True, "message": "Student updated successfully"}
    
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    
    finally:
        session.close()

#Delete a row from database
def delete_password_row(student_id):
    session = Session()

    #Finds the student record with specified studentID    
    try:
        query = sa.select(StudentCredentials).where(StudentCredentials.studentID == student_id)
        row = session.execute(query).scalar_one_or_none()

        #Checks if student exists
        if row is None:
            return {"succes": False, "error": "Student not found"}
        
        #deletes specified row
        session.delete(row)
        session.commit()
        return {"success": True, "message": "Student deleted successfully"}
    
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    
    finally:
        session.close()