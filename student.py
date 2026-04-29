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

class gradeManager():

    #Function to change percentage into GPA scale
    def calculate_to_GPA(grade):
        if grade is None:
            return None
        grade = float(grade)

        if grade >= 90:
            return 4.0
        if grade >= 80:
            return 3.0
        if grade >= 70:
            return 2.0
        if grade >= 60:
            return 1.0
        else:
            return 0.0
        
    #Function to get grades and convert them to GPA
    def get_student_grades(studentID):
        #Import the student data
        from data_handler import getGrades

        #Creates a list of Grades now in GPA scale
        grades = [
            gradeManager.calculate_to_GPA(getGrades(studentID, "math")),
            gradeManager.calculate_to_GPA(getGrades(studentID, "programming")),
            gradeManager.calculate_to_GPA(getGrades(studentID, "science"))
            ]
        #Remove any missing grades
        grades = [g for g in grades if g is not None]
        #Returns a 2D list of grades
        return [grades]

    #Function to calculate average from grades
    def calculate_average(grades):
        if not grades:
            return None

        total = 0
        count = 0

        for row in grades:
            for value in row:
                total += value
                count += 1

        return total / count

