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
    def __init__(self, studentID: int, name: str, age: int, gender: str, phoneNumber: str, grade: int, adminStatus: bool):
        self.studentID = studentID
        self.name = name
        self.age = age
        self.gender = gender
        self.phoneNumber = phoneNumber
        self.grade = grade
        self.adminStatus = adminStatus

#Gradmanger class
class GradeManager():

    #Initilizer
    def __init__(self, numberOfStudents: int, numberOfAssignments: int):
        self.grades = [
            [None for _ in range(numberOfAssignments)]
            for _ in range(numberOfStudents)]
    
    #sets grade at grades[studentindex][assignmentIndex]
    def set_grades(self, studentIndex: int, assignmentIndex: int, grade: int):
        self.grades[studentIndex][assignmentIndex] = grade

    #Returns grade from grades[studentIndex][assignmentIndex]
    def get_grade(self, studentIndex: int, assignmentIndex: int):
        return self.grades[studentIndex][assignmentIndex]
    
    #Returns grades from grades[studentIndex]
    def get_all_grades(self, studentIndex: int):
        return self.grades[studentIndex]
    
    #Calculates average grade for grades[studentIndex]
    def calculate_average(self, studentIndex: int):
        row = self.grades[studentIndex]
        validGrades = [g for g in row if g is not None]
        if not validGrades:
            return 0
        return sum(validGrades) / len(validGrades)