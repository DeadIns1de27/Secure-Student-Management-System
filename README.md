# **Secure-Student-Management-System**

A professional-grade, modular Python application that serves as a secure repository for academic data. The features of this application include a GUI, data visualization with matplotlib, a SQL serverless database, 2-factor authentication, and salting.



###### **Table of Contents**

* Introduction
* Additional Features List
* Installation
* Usage
* File Descriptions





###### **Introduction**

The Secure-Student-Management-System is an application that focuses on a secure repository for academic data. It allows users to register, log in, and view student records. In addition, it allows admins to create, edit, delete, and view student records. This application features safety precautions to safely secure student records in a serverless database. Users access this application through a GUI.





###### **Additional Features**

1. GUI with Tkinter
2. Data Visualization
3. SQL serverless database
4. Two-Factor Authentication QR code
5. Salting





###### **Installation / Requirements**

* sqlalchemy
* numpy
* pyotp
* qrcode





###### **How to Run Application**

To run this application, you must first download all the necessary requirements. This includes sqlalchemy, numpy, pyotp, and qrcode. To launch this application, run the gui.py file. The application will then open a window. Users are able to select log in or register. New students can register and input their information to create an account. If you are an existing user, you can enter your student ID and password. Once you register or log in, the students can view their records. If you are an admin, you will be able to edit, add, delete, or view student records. Users can log out using the log out button. Close the application by pressing the X in the top right corner.





###### **Main Files**

1. main.py
2. session\_manager.py
3. user.py
4. student.py
5. validator.py
6. security.py
7. data\_handler.py
8. gui.py
9. two\_factor\_authentication.py





##### **File Descriptions**

###### main.py

* Entry point that controls program flow.



###### session\_manager.py

* This file tracks login attempts and increments after a failed attempt. After three failed attempts, the system will not allow the user to try again.



###### user.py

* The User class will define core attributes such as email and hashed password. It will define user, admin, and StudentUser access as they inherit from the user class. Using data\_handler to save, edit, delete, and view student records.



###### student.py

* Student will define data objects for students, including a unique 700 number, name, age(16-100), gender, and phone number. Defines the grade manager to perform calculations. For example, calculate\_average.



###### validator.py

* The validator file will use regex to validate each string the user inputs. For example, capitalization of names, valid phone numbers, email extensions, and passwords.



###### security.py

* The security file will hash passwords and have a verify function. This file is focused on SHA-256 hashing and salting.



###### data\_handler.py

* This is the storage layer that will store the student record in a serverless database (SQLite). It has the following functions, save\_student, load\_student, update\_student, delete\_student, save\_password, load\_password, update\_password, delete\_password\_row, validate\_login, and getGradesArray.



###### gui.py

* The graphical interface is located in this file. It handles the layout and windows of the application. It allows users to input information that is then stored in the database. It handles buttons and event handlers.



###### two\_factor\_authentication.py

* The two-factor authentication file uses Google Authenticator via the pyotp library. Included in this file are the following functions: generate\_user\_key, display\_qr\_code, and verify\_key.

