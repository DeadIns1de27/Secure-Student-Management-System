"""
Description:
File dedicated to handling Graphical Interface
Should Include:
1. Windows / frames / layouts
2. Buttons, labels, entry fields
3. Event handlers (button clicks)
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import validator as v
import data_handler as dh
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from two_factor_authentication import TwoFactorAuthentication
from session_manager import SessionManager

#Font and size for titles
LARGEFONT =("Times New Roman", 35)

#Main app class: controls each frame displayed
class AppGui(tk.Tk):

    #Initialize the gui
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.title("Secure Student Management System")  #App window title

        self.geometry("800x800")    #App window size

        self.current_user = None    #stores current user id

        self.adminStatus = None     #stores id admin status

        #Create a container to store the different frames being displayed
        container = tk.Frame(self)
        container.pack(side= 'top', fill= 'both', expand= True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        #create each frame and store
        #Note: Add new frame class into this
        for F in (LoginFrame, StudentFrame, AdminFrame, RegisterFrame, twoFactorFrame, welcomeFrame, VisualizationFrame):
 
            frame = F(container, self)
 
            # initializing frame of that object for each page with for loop
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        self.show_frame(welcomeFrame)     #Default frame is welcome page

        self.session_manager = SessionManager()     #Track the login session

    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]

        #if frame has function load_data, run it
        if hasattr(frame, "load_data"):
            frame.load_data()

        frame.tkraise()
        
#Main Base frame for all frames for tidier grid 
class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.form = tk.Frame(self)
        self.form.grid(row=0, column=0)

    #check if the chracter is a digit, if not chracter becomes empty
    def only_digits(self, value):
        return value.isdigit() or value == ""
    
    #check if the chracter being entered into entry box is digit
    def digit_validator(self):
        return (self.register(self.only_digits), "%P")
    
    #format the phone entry from xxxxxxxxxx to xxx-xxx-xxxx
    def format_phone(self, value):
    
        # remove anything that isn't a digit
        digits = "".join(filter(str.isdigit, value))

        # limit to 10 digits
        digits = digits[:10]

        # format
        if len(digits) <= 3:
            return digits
        elif len(digits) <= 6:
            return f"{digits[:3]}-{digits[3:]}"
        else:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        
    #Event handler that checks user input
    def on_phone_change(self, event):

        value = self.phone_number.get()

        formatted = self.format_phone(value)

        self.phone_number.delete(0, "end")
        self.phone_number.insert(0, formatted)

    #get the user record from the database
    def get_current_student(self):
        from data_handler import load_student
        return load_student(self.controller.current_user)
    
    #Creates a back button at the bottom left of the frame
    def create_back_button(self, target_frame):
        ttk.Button(self.form, text="← Back", command=lambda: self.controller.show_frame(target_frame)).grid(row=99, column=0, padx=10, pady=10, sticky="w")
    
    #clears the widgets in the frame
    def reset_frame(self):
        for widget in self.form.winfo_children():
            widget.destroy()


#Login Frame
class LoginFrame(BaseFrame):
    def __init__(self, parent, controller): 
        super().__init__(parent, controller)

        self.create_back_button(welcomeFrame)   #back button

        # label of title
        ttk.Label(self.form, text ="Login", font = LARGEFONT).grid(row= 0, column= 4, padx= 10, pady= 10)
        
        # Label and entry box for student id
        ttk.Label(self.form, text="Student ID").grid(row= 2, column= 4, padx = 10)
        self.studentID = ttk.Entry(self.form, validate="key", validatecommand=self.digit_validator())
        self.studentID.grid(row= 3, column= 4, padx = 10, pady= 10)

        # Label and entry box for password
        ttk.Label(self.form, text="Password").grid(row= 5, column= 4, padx = 10)
        self.password = ttk.Entry(self.form, show= "*")
        self.password.grid(row= 6, column= 4, padx = 10, pady= 10)

        #Button to confirm login
        ttk.Button(self.form, padding= (5, 7), text="Login", command= self.login).grid(row= 7, column= 4, padx = 10, pady= 10)

    # Function to check the login status
    def login(self):

        # Get student id and password from entry box
        studentID = self.studentID.get().strip()
        password = self.password.get().strip()

        # Validate format for studentID and password
        #if id or password do not match requirements, return
        if not v.validate_id(studentID):
            messagebox.showerror("Invalid Student ID", "Student ID does not fit criteria. Please try again.")
            return

        if not v.validate_password(password):
            messagebox.showerror("Invalid Password", "Password does not fit criteria. Please try again.")
            return

        #Call track_login_attempts to get the status (admin/student/failed login)
        self.controller.adminStatus = self.controller.session_manager.track_login_attempts(studentID.strip(), password.strip())

        #check status and show student/admin frame
        #if password is incorrect or they are locked out, return an error message
        if self.controller.adminStatus == "Incorrect":
            messagebox.showerror("Login Failed", "Incorrect login. Please try again.")
            return

        elif self.controller.adminStatus == "Locked":
            messagebox.showerror("Account Locked", "Too many failed login attempts.")
            self.controller.show_frame(welcomeFrame)
            return

        else:
            self.controller.current_user = studentID
            self.controller.show_frame(twoFactorFrame)

#Register Frame
class RegisterFrame(BaseFrame):
    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        self.create_back_button(welcomeFrame)   #back button

        #Label for title
        ttk.Label(self.form, text ="Register", font = LARGEFONT).grid(row= 0, column= 4, padx= 10, pady= 10)

        #Label and entry for name
        ttk.Label(self.form, text="Name").grid(row= 2, column= 4, padx = 10)
        self.name = ttk.Entry(self.form)
        self.name.grid(row= 3, column= 4, padx = 10, pady= 10)

        #label and entry for age
        ttk.Label(self.form, text="Age").grid(row= 5, column= 4, padx = 10)
        self.age = ttk.Entry(self.form, validate="key", validatecommand= self.digit_validator())
        self.age.grid(row= 6, column= 4, padx = 10, pady= 10)

        #label and entry for gender
        ttk.Label(self.form, text="Gender").grid(row= 7, column= 4, padx = 10)
        self.gender = ttk.Entry(self.form)
        self.gender.grid(row= 8, column= 4, padx = 10, pady= 10)

        #label and entry for phone number
        ttk.Label(self.form, text="Phone Number").grid(row= 9, column= 4, padx = 10)
        self.phone_number = ttk.Entry(self.form, validate="key", validatecommand= self.digit_validator)
        self.phone_number.bind("<KeyRelease>", self.on_phone_change)
        self.phone_number.grid(row= 10, column= 4, padx = 10, pady= 10)

        #label and entry for email
        ttk.Label(self.form, text="Email").grid(row= 11, column= 4, padx = 10)
        self.email = ttk.Entry(self.form)
        self.email.grid(row= 12, column= 4, padx = 10, pady= 10)

        #label and entry for password
        ttk.Label(self.form, text="Password").grid(row= 13, column= 4, padx = 10)
        self.password = ttk.Entry(self.form, show= "*")
        self.password.grid(row= 14, column= 4, padx = 10, pady= 10)

        #label and entry for password confirmation
        ttk.Label(self.form, text="Confirm Password").grid(row= 15, column= 4, padx = 10)
        self.confirmed = ttk.Entry(self.form, show= "*")
        self.confirmed.grid(row= 16, column= 4, padx = 10, pady= 10)

        #Button to register student info
        ttk.Button(self.form, text="Register Now", padding= (7, 10), command= lambda: self.register_info()).grid(row= 17, column= 4, padx = 10, pady= 10)

    #function ran when register button is pressed
    def register_info(self):

        #Import functions used only in this function call
        from data_handler import save_student, save_password
        import student
        from security import hash_password

        error = []

        #Check if the 2 password matches
        if self.confirmed.get().strip() != self.password.get().strip():
            messagebox.showerror("Mismatched Passwords", "Passwords do not match. Please try again.")
            return

        #Check validation for name, email, phone, password
        if not v.validate_name(self.name.get().strip()):
            error.append("Name initials must be capitalized. ")
        
        if not v.validate_email(self.email.get().strip()):
            error.append("Email must only contain accepted domains (gmail.com/yahoo.com/ucmo.edu). ")
        
        if not v.validate_phone(self.phone_number.get().strip()):
            error.append("Phone number must be in ###-###-#### format. ")
        
        if not v.validate_password(self.password.get().strip()):
            error.append("Password must begin with a special character and be 6 - 12 characters long. ")

        if error:
            error_message = "\n".join(error)
            messagebox.showerror("Invalid Registration", error_message)
            return

        #store the student records
        record = student.StudentRecord(
            studentID= student.StudentRecord.studentID_generator(),
            name= self.name.get().strip(),
            age= self.age.get().strip(),
            gender= self.gender.get().strip(),
            phoneNumber= self.phone_number.get().strip(),
            email= self.email.get().strip()
        )
        
        #Try to save the studen records and hashed password into the database and goes to student page when succeeds
        try:
            save_student(record)
            save_password(record.studentID, hash_password(self.password.get().strip()))
            print("Account Created")
            self.controller.current_user = record.studentID
            self.controller.show_frame(twoFactorFrame)

        except ValueError as e:
            print(e)        

#Admin Page
class AdminFrame(BaseFrame):
    def __init__(self, parent, controller):
        from student import gradeManager
        super().__init__(parent, controller)

        #Title label
        ttk.Label(self.form, text ="Admin Page", font = LARGEFONT).grid(row = 0, column = 0, columnspan= 2, padx = 10, pady= 10)

        #Student Id entry
        ttk.Label(self.form, text = "Enter Student ID").grid(row = 1, column = 0, padx = 10, pady= 10)
        self.entry = ttk.Entry(self.form)
        self.entry.grid(row = 2, column = 0, padx = 10, pady= 10)

        #submit button
        ttk.Button(self.form, padding= (5, 7), text = "Submit", command = self.displayStudent).grid(row = 2, column = 1, sticky = "w", padx = 10, pady= 10)

        #Edit button
        self.editButton = ttk.Button(self.form, padding= (5, 7), text = "Edit", command = self.editStudent)
        self.editButton.grid(row = 5, column = 1, padx = 10, pady= 10)
        self.editButton.grid_remove()

        #delete button
        self.deleteButton = ttk.Button(self.form, padding= (5, 7), text = "Delete", command = self.deleteStudent)
        self.deleteButton.grid(row = 3, column = 1, sticky = "w", padx = 10, pady= 10)
        self.deleteButton.grid_remove()

        #Visualization button
        ttk.Button(self.form, padding= (5, 7), text = "Visualization", command = lambda: self.controller.show_frame(VisualizationFrame)).grid(row = 5, column = 0, padx = 10, pady= 10)

        #Button to log out
        ttk.Button(self.form, text="Log Out", padding=(5, 7), command= lambda: self.controller.show_frame(LoginFrame)).grid(row = 6, column = 0, padx = 10, pady = 10)
        
        self.data_frame = tk.Frame(self.form, bd = 2, relief = "groove", padx = 10, pady = 10)
        self.data_frame.grid(row = 4, column = 0, columnspan = 2, padx = 10, pady= 10)

        self.grade = gradeManager()
        
    #Displays student info
    def displayStudent(self):

        #Gets student data from database
        enteredID = self.entry.get()
        student = dh.load_student(enteredID)
        if student == None:
            messagebox.showerror("Error", "Student doesen't exist")
            return None

        #Clears old data
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        #Displays student data
        row = 0
        for key, value in student.items():
            ttk.Label(self.data_frame, text = f"{key}").grid(row = row, column = 0, sticky = "w", padx = 5, pady = 2)
            ttk.Label(self.data_frame, text = str(value)).grid(row = row, column = 1, sticky = "w", padx = 5, pady = 2)
            row += 1

        #Shows student average gpa across 3 subjects
        ttk.Label(self.data_frame, text = "Average GPA:").grid(row = row, column = 0, sticky = "w", padx = 5, pady = 2)
        ttk.Label(self.data_frame, text = round(self.grade.calculate_average(enteredID), 2)).grid(row = row, column = 1, sticky = "w", padx = 5, pady = 2)

        self.currentData = student

        self.editButton.grid()
        self.deleteButton.grid()

    #edit student details
    def editStudent(self):

        #Clear frame
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        self.edit_entries = {}

        #Loop through the student record to edit
        row = 0
        for key, value in self.currentData.items():

            if key == "studentID":      #Cant edit student ID
                continue

            ttk.Label(self.data_frame, text = f"{key}").grid(row = row, column = 0, sticky = "w", padx = 10, pady= 10)

            entry = ttk.Entry(self.data_frame)
            entry.insert(0, str(value))
            entry.grid(row = row, column = 1, sticky = "w", padx = 10, pady= 10)

            self.edit_entries[key] = entry
            row += 1

        #Save edit button
        self.editButton.config(text = "Save", command = self.saveStudent)

    #Save edited info into database
    def saveStudent(self):
        studentID = self.currentData["studentID"]

        updates = {}
        for key, entry in self.edit_entries.items():
            if key == "studentID":
                continue

            value = entry.get()

            if key == "adminStatus":
                if value.lower() in ("true", "1", "yes"):
                    value = True
                elif value.lower() in ("false", "0", "no"):
                    value = False
                else:
                    print("Invalid bolean value")
                    return
            
            if key in ("age", "grade"):
                try:
                    value = int(value)
                except ValueError:
                    print(f"{key} must be a number")
                    return
                          
            updates[key] = value

        result = dh.update_student(studentID, **updates)

        if result["success"]:
            print("Updated successfully")
        else:
            print("Error:", result["error"])

        self.displayStudent()

        self.editButton.config(text = "Edit", command = self.editStudent)

    #Delete entire student record from database
    def deleteStudent(self):

        studentID = self.currentData["studentID"]

        dh.delete_student(studentID)

        #Clear frame
        for widget in self.data_frame.winfo_children():
            widget.destroy()
            
#Student page
class StudentFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        #Create Student Page Label
        ttk.Label(self.form, text ="Student Page", font = LARGEFONT).grid(row = 0, column = 4, columnspan=2, padx = 10, pady = 10)        
        ttk.Button(self.form, padding= (5, 7), text= "Log Out", command=lambda: self.controller.show_frame(LoginFrame)).grid(row= 20, column= 4, columnspan=2, padx= 10, pady= 10)

    #Function that loads user ID from login
    def load_data(self):
    #Get the student record
        from student import gradeManager

        self.grade = gradeManager()
        self.record = self.get_current_student()
        student = self.controller.current_user
        row = 1

        ttk.Label(self.form, text="Average GPA:", width=20, anchor="w").grid(row=11, column=4, sticky="w", padx = 10, pady= 10)
        ttk.Label(self.form, text=round(self.grade.calculate_average(student), 2)).grid(row=11, column=5, sticky="w", padx = 10, pady= 10)

        #Loop through all the records and display the label and the key
        for label, key in self.record.items():
            
            if label == "adminStatus":
                continue

            ttk.Label(self.form, text=f"{label}:", width=20, anchor="w").grid(row=row, column=4, sticky="w", padx = 10, pady= 10)

            ttk.Label(self.form, text= key).grid(row=row, column=5, sticky="w", padx = 10, pady= 10)

            row += 1
        
#Grade Visualization frame
class VisualizationFrame(BaseFrame):
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.create_back_button(AdminFrame) #back button

        #label for Data Visualization
        ttk.Label(self.form, text = "Data Visualization", font = LARGEFONT).grid(row = 0, column = 1, padx = 10, pady= 10)

        #Label for class name
        ttk.Label(self.form, text = "Enter Class Name").grid(row = 1, column = 1, padx = 10, pady= 10)

        #Entry box for class name
        self.entry = ttk.Entry(self.form)
        self.entry.grid(row = 2, column = 1, padx = 10, pady= 10)

        #confirm classname
        ttk.Button(self.form, text = "Submit", command = self.showVisual).grid(row = 2, column = 2, padx = 10, pady= 10)
    
    #Displays graph
    def showVisual(self):

        #Creates a figure
        fig = Figure(figsize = (5, 4), dpi = 100)
        ax = fig.add_subplot()

        #Takes cleaned input and returns grades as array
        className = self.entry.get().lower().strip()
        arr = dh.getGradesArray(className)
        
        #Checks if arr is empty
        if arr is None:
            messagebox.showerror("Error", "Class doesn't exist")
            return None

        #Creates the histogram
        ax.hist(arr)
        ax.set_title("Grade Distribution")

        #Turns matplotlib figure into tkinter widget
        canvas = FigureCanvasTkAgg(fig, master = self.form)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 4, column = 1, padx = 10, pady= 10)


#2 Factor Authentication frame
class twoFactorFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.attempts = 0       #Tracks OTP attempts
        self.tfa = TwoFactorAuthentication()

    #Runs immediately upon show frame
    def load_data(self):
        from data_handler import load_twoFA_key
        self.reset_frame()      #Clear widgets from previous use

        self.student = self.controller.current_user     #store student id

        self.secret_key = load_twoFA_key(self.student)  #get student 2fa key from database

        #if no key, means initial setup, if has key, means normal login
        try:
            if self.secret_key is None:
                self.show_qr_code()
            else:
                self.hide_qr_code()

        except Exception as e:
            return e

    #Initial Setup
    def show_qr_code(self):
        from data_handler import save_twoFA_key

        #Label for frame
        ttk.Label(self.form, text= "Scan The QR Code", font= LARGEFONT).grid(row = 0, column = 4, columnspan=2, padx = 10, pady = 10)

        #Displays the student id that was generated
        ttk.Label(self.form, font=(15), text= f"Your student ID is {self.student}").grid(row = 1, column = 4, columnspan=2, padx = 10, pady = 10)

        #Create Qr Code label to display image
        self.qr_label = ttk.Label(self.form)
        self.qr_label.grid(row=2, column=4, columnspan=2, padx = 10, pady= 10)

        self.secret_key = self.tfa.generate_user_key()      #Generate a 2fa key

        save_twoFA_key(self.student, self.secret_key)       #save the key to the database

        self.display_qr_image(self.secret_key, self.student)    #Display the qr code

        #Switches frame to log in
        ttk.Button(self.form, padding=(5, 7), text="Log In", command=lambda: self.controller.show_frame(LoginFrame)).grid(row=4, column=4, columnspan=2, padx = 10, pady= 10)

    #Normal login procedure
    def hide_qr_code(self):
        
        #Label for normal login
        ttk.Label(self.form, text= "Enter The OTP", font= LARGEFONT).grid(row = 0, column = 4, columnspan=2, padx = 10, pady = 10)

        # OTP entry 
        self.code_entry = ttk.Entry(self.form)
        self.code_entry.grid(row=3, column=4, columnspan=2, padx = 10, pady= 10)

        # otp entry status
        self.status_label = ttk.Label(self.form, text="")
        self.status_label.grid(row=5, column=4, columnspan=2, padx = 10, pady= 10)

        #Verify if the otp is correct
        ttk.Button(self.form, padding=(5,7), text="Verify", command= self.on_verify).grid(row=4, column=4, columnspan=2, padx = 10, pady= 10)

    #Displays the actual image
    def display_qr_image(self, key, student):
        
        self.qr_photo = self.tfa.display_qr_code(key, student)

        self.qr_label.config(image= self.qr_photo)
        self.qr_label.image = self.qr_photo

    #Runs the verification for otp and key linked to student id
    def on_verify(self):

        code = self.code_entry.get().strip()
        if self.tfa.verify_key(self.secret_key, code):

            self.status_label.config(text= "Success!")

            self.route_user()   #Route user to either student frame or admin frame

        else:
            
            #Tracks attemps for otp
            self.attempts += 1
            self.status_label.config(text= "Incorrect Code")

            if self.attempts >= 3:
                self.status_label.config(text= "Too many attempts")
                self.controller.show_frame(welcomeFrame)

    #Route user based on their admin status
    def route_user(self):

        if self.controller.adminStatus == "Admin":
            self.controller.show_frame(AdminFrame)

        elif self.controller.adminStatus == "Student":
            self.controller.show_frame(StudentFrame)

#Welcome Frame (Initial Frame)     
class welcomeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        #Label and button
        ttk.Label(self.form, text= "Welcome To UCM", font= LARGEFONT).grid(row = 1, column = 4, columnspan=2, padx = 10, pady = 10)
        ttk.Button(self.form, text="Login", width=20, padding= (5, 10), command=lambda: self.controller.show_frame(LoginFrame)).grid(row = 3, column = 2, columnspan=3, padx = 10, pady= 10)
        ttk.Button(self.form, text="Register", width= 20, padding= (5, 10), command=lambda: self.controller.show_frame(RegisterFrame)).grid(row = 3, column = 5, columnspan=3, padx = 10, pady= 10)

        #Image
        full_sized_image = tk.PhotoImage(file = "UCMlogo.png")
        self.ucm_logo = full_sized_image.subsample(x = 5, y = 5)
        ttk.Label(self.form, image = self.ucm_logo).grid(row = 2, column = 4, columnspan = 2, padx = 10, pady = 10)
