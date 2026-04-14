'''
user.py layer

Will include the user class.
- Defines emails and hash passwords
Will include the Admin class.
- Defines access to add, edit, and delete a user
Will include the StudentUser class.
- Defines a student to VIEW only access to their record

'''

#import StudentRecord
from student import StudentRecord

#User class
class User:
    #Initializer
    def __init__(self, email, hash_password):
        self.email = email
        self.hash_password = hash_password

#List to store student temp
student_list = []

#Admin class
class Admin(User):
    #Add a new student to the list
    def add_student(self, studentID: int, name: str, age: int, gender: str, phoneNumber: str):
        new_student = StudentRecord(studentID, name, age, gender, phoneNumber)
        student_list.append(new_student) #Add the new student to the student_list
        return "New student added"

    #Edit student information
    def edit_student(self, studentID, name=None, age=None, gender=None, phoneNumber=None):

        #for loop to go through students
        for student in student_list:

            #Checks to find the right student with studentID
            if student.studentID == studentID:
                if name is not None:
                    student.name = name
                if age is not None:
                    student.age = age
                if gender is not None:
                    student.gender = gender
                if phoneNumber is not None:
                    student.phoneNumber = phoneNumber
                return "student edited"
        return "Student not found"

    #Delete student and information
    def delete_student(self,studentID):

        #Loop through students
        for student in student_list:
            if student.studentID == studentID:
                student_list.remove(student) #Remove the student from the list
                return "student deleted"
        return "Student not found"



#StudentUser class
class StudentUser(User):
    #Create the view_student_record
    def view_student_record(self, studentID):

        #loop through the list
        for student in student_list:
            #find the correct matching studentID
            if student.studentID == studentID:
                #Return the student object
                return student
        return "Student not found"



