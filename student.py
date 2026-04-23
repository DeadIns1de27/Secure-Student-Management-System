'''
Data Layer:

StudentRecord Class: Defines the data object for students including 
unique 700 number, name, age(16-100), gender, phone number.

GradeManager: Dedicated module to handle 2D lists of grades and 
perform calculations like calculate_average.
'''

from random import randint

#StudentRecord class
class StudentRecord():

    #Initilizer
    def __init__(self, studentID: int, name: str, age: int, gender: str, phoneNumber: str, email: str):
        self.studentID = studentID
        self.name = name
        self.age = age
        self.gender = gender
        self.phoneNumber = phoneNumber
        self.email = email
        self.grade = "N/A"
        self.adminStatus = False

    #Generates a unique id that isnt registered in the database
    def studentID_generator(self):
        
        #Import load student in this call
        from data_handler import load_student

        while True:
            number = randint(0, 999999)

            self.studentID = f"700{number:06d}"

            if load_student(self.studentID) is None:
                return self.studentID