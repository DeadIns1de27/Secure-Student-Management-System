'''
user.py layer

Will include the user class.
- Defines emails and hash passwords

Will include the Admin class.
- Defines access to add, edit, and delete a user
- Allow for the user to view student records

Will include the StudentUser class.
- Defines a student to VIEW only access to their record

'''

#import StudentRecord
from student import StudentRecord
from data_handler import save_student, delete_student, load_student, update_student

#User class
class User:
    #Initializer
    def __init__(self, email, hash_password):
        self.email = email
        self.hash_password = hash_password


#Admin class
class Admin(User):
    #Add a new student to the list
    def add_student(self, studentID: int, name: str, age: int, gender: str, phoneNumber: str):
        new_student = StudentRecord(studentID, name, age, gender, phoneNumber)
        save_student(new_student)
        return "New student added"

    #Edit student information
    def edit_student(self, studentID, name=None, age=None, gender=None, phoneNumber=None):
        #Update the student
        return update_student(
            studentID,
            name=name,
            age=age,
            gender=gender,
            phone=phoneNumber
        )

    #Delete student and information
    def delete_student_record(self,studentID):

        #Check for student
        student = load_student(studentID)

        #Make sure the student is valid
        if student is None:
              return "Student not found"

        #Delete the student if found
        return delete_student(studentID)


#StudentUser class
class StudentUser(User):
    #Create the view_student_record
    def view_student_record(self, studentID):
        #Find the student record
        student = load_student(studentID)

        #Makes sure student is valid
        if student is None:
            return "Student not found"
        #Returns the student
        return student



