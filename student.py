'''
Data Layer:

StudentRecord Class: Defines the data object for students including 
unique 700 number, name, age(16-100), gender, phone number.

GradeManager: Dedicated module to handle 2D lists of grades and 
perform calculations like calculate_average.
'''

#StudentRecord class
class StudentRecord():

    #Initilizer
    def __init__(self, studentID: int, name: str, age: int, gender: str, phoneNumber: str, email: str, grade: int, adminStatus: bool):
        self.studentID = studentID
        self.name = name
        self.age = age
        self.gender = gender
        self.phoneNumber = phoneNumber
        self.email = email
        self.grade = grade
        self.adminStatus = adminStatus