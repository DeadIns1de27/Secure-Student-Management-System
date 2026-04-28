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
        self.adminStatus = False
        self.mathGrade = 0
        self.programmingGrade = 0
        self.scienceGrade = 0

    #Generates a unique id that isnt registered in the database
    @staticmethod
    def studentID_generator():
        
        #Import load student in this call
        from data_handler import load_student

        while True:
            number = randint(0, 999999)

            studentID = f"700{number:06d}"

            if load_student(studentID) is None:
                return studentID