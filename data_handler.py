'''
Storage Layer:

sqlalchemy used to store data objects in 
a serverless database (sqlite) titled database.db
'''

#Import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

#Import password hash verification
from security import verify_password

#Sets databases file location
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

#Imports numpy
import numpy as np

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
    email = sa.Column(sa.String)
    adminStatus = sa.Column(sa.Boolean)
    mathGrade = sa.Column(sa.Integer)
    programmingGrade = sa.Column(sa.Integer)
    scienceGrade = sa.Column(sa.Integer)

#Stores studentID and hased password
class StudentCredentials(Base):

    #Table name
    __tablename__ = "student_creds"

    #Columns
    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    studentID = sa.Column(sa.Integer, sa.ForeignKey("student_info.studentID"))
    password = sa.Column(sa.String)
    twoFA_key = sa.Column(sa.String)

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
                                email = record.email,
                                adminStatus = record.adminStatus,
                                mathGrade = record.mathGrade,
                                programmingGrade = record.programmingGrade,
                                scienceGrade = record.scienceGrade)
    
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
def load_student_grade(student_id: int) -> int | None:
    session = Session()

    try:
        #Finds the student record with specified studentID
        student = sa.select(StudentTable.grade).where(StudentTable.studentID == student_id)
        row = session.execute(student).scalar_one_or_none()

        if row is None:
            return None
    
        #Returns specified student record
        return row

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

#Adds a key to the database
def save_twoFA_key(student_id, key):
    session = Session()

    try:
        query = sa.select(StudentCredentials).where(StudentCredentials.studentID == student_id)
        row = session.execute(query).scalar_one_or_none()

        if row is None:
            return None
        
        row.twoFA_key = key

        session.commit()

        return {"success": True, "message": "Saved 2FA key"}
    
    except Exception as e:
        session.rollback()
        return e
    
    finally:
        session.close()

#Loads the key saved in the database
def load_twoFA_key(student_id):
    session = Session()

    try:
        query = sa.select(StudentCredentials.twoFA_key).where(StudentCredentials.studentID == student_id)
        row = session.execute(query).scalar_one_or_none()

        if row is None:
            return None
        
        return row
    
    except Exception as e:
        session.rollback()
        return e

    finally:
        session.close()

#checks the user password and also their status(admin / student)
def validate_login(student_id, input_password) -> str:
    session = Session()

    try:
        #loads user password associated with id
        password = load_password(student_id)

        #check if theres a password
        if not password:
            return None
        
        #check if the input password matches the stores password
        if not verify_password(password, input_password):
            return None
        
        #get the adminstatus of the id from the database
        query = sa.select(StudentTable.adminStatus).where(StudentTable.studentID == student_id)
        adminStatus = session.execute(query).scalar_one_or_none()

        #check if user is admin or student
        if adminStatus:
            return "Admin"
        return "Student"

    except Exception as e:
        session.rollback()
        return None

    finally:
        session.close()

def getGrades(student_id, class_subject: str):
    session = Session()
    class_subject = class_subject.lower().strip()
    try:
        match class_subject:
            case "math":
                query = sa.select(StudentTable.mathGrade).where(StudentTable.studentID == student_id)
            case "programming":
                query = sa.select(StudentTable.programmingGrade).where(StudentTable.studentID == student_id)
            case "science":
                query = sa.select(StudentTable.scienceGrade).where(StudentTable.studentID == student_id)
            case _:
                print("No subject found")

        classScore = session.execute(query).scalar_one_or_none()

        return int(classScore)
    
    except Exception as e:
        session.rollback()
        return None
    
    finally:
        session.close()

def getGradesArray(className: str):

    session = Session()

    className = className.lower()
    try:
        match className:
            case "math":
                query = StudentTable.mathGrade
            case "programming":
                query = StudentTable.programmingGrade
            case "science":
                query = StudentTable.scienceGrade
            case _:
                print("No subject found")

        rows = session.query(query).all()

        arr = np.array(rows)

        return arr
    
    except Exception as e:
        session.rollback()
        return None
    
    finally:
        session.close()

getGradesArray("math")