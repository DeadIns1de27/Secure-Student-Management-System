'''
Description:
main folder to control program flow

test
test2
test3 (marcus)
test4

Skeleton Code for main.py with unbuilt functions
'''
from user import User
from session_manager import SessionManager
import sys
from admin import AdminRecord
from student import StudentRecord

#welcome screen goes here first
print("Welcome to Secure Student Management System")
print("-------------------------------------------")
print("1. Register")
print("2. Login")
print("3. Exit")
user_selection = "0"

#while loop that continues until user clicks exit button
while user_selection != "3. Exit":

    user_selection = input("Enter your choice: ")
    if user_selection == "1. Register":
        #call the register_manager function
        register_manager():
        '''
        Things user must enter to register
        1. First Name (Capital first letter, at least 2 letters long, no digits/special characters)
        2. Last Name (Capital last letter, at least 2 letters long, no digits/special characters)
        3. Age (16 - 100)
        4. Gender
        5. Phone Number (xxx-xxx-xxxx format)
        6. Email (@yahoo.com, .@gmail.com, .@ucmo.edu format only)
        7. Password (Start with special character !@#$%^&* and be 6 - 12 characters long)
        
        Inform the user if they incorrectly input anything
        Generate the user a unique 700xxxxxx number 
        
        '''
        #Make user enter first name, last name
    elif user_selection == "2. Login":
        #if the maximum attempts are reached, exit the program
        if not SessionManager():
            sys.exit()

    #welcome the user with their name
    welcome_user(name)

    #check to see whether user is admin or student, return correct class
    if User == admin:
        AdminRecord(User)
        #Admin will be prompted to select a student's record
        #and whether they would like to view, edit, or delete
        student_lookup_number = int(input("Enter student's 700xxxxxx number: "))
        if student_lookup_number in list_of_students:
            StudentRecord(student_lookup_number)

    else:
        StudentRecord(User)
        #Show user all of the student's records.
        #This includes, name, age, gender, classes registered, grades, and grade averaeg

sys.exit()