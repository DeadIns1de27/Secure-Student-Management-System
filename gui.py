"""
Description:
File dedicated to handling Graphical Interface
Should Include:
1. Windows / frames / layouts
2. Buttons, labels, entry fields
3. Event handlers (button clicks)
"""

import tkinter as tk
import validator as v

#Font and size for titles
LARGEFONT =("Times New Roman", 35)

#Main app class: controls each frame displayed
class AppGui(tk.Tk):

    #Initialize the gui
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.title("Secure Student Management System")  #App window title

        self.geometry("800x600")    #App window size

        #Create a container to store the different frames being displayed
        container = tk.Frame(self)
        container.pack(side= 'top', fill= 'both', expand= True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        #create each frame and store
        #Note: Add new frame class into this
        for F in (LoginFrame, StudentFrame, AdminFrame, RegisterFrame):
 
            frame = F(container, self)
 
            # initializing frame of that object for each page with for loop
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        self.show_frame(AdminFrame)     #Default frame is login
 
    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
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
        
    #Event handler that
    def on_phone_change(self, event):

        value = self.phone_number.get()

        formatted = self.format_phone(value)

        self.phone_number.delete(0, "end")
        self.phone_number.insert(0, formatted)


#Login Frame
class LoginFrame(BaseFrame):
    def __init__(self, parent, controller): 
        super().__init__(parent, controller)

        # label of title
        tk.Label(self.form, text ="Login", font = LARGEFONT).grid(row= 0, column= 4, padx= 10, pady= 10)
        
        # Label and entry box for student id
        tk.Label(self.form, text="Student ID").grid(row= 2, column= 4)
        self.studentID = tk.Entry(self.form, validate="key", validatecommand=self.digit_validator())
        self.studentID.grid(row= 3, column= 4)

        # Label and entry box for password
        tk.Label(self.form, text="Password").grid(row= 5, column= 4)
        self.password = tk.Entry(self.form, show= "*")
        self.password.grid(row= 6, column= 4)

        #Button to confirm login
        tk.Button(self.form, text="Login", command= self.login).grid(row= 7, column= 4, pady= 10)

        #Button to register a new account
        tk.Button(self.form, text="Register Account", command= lambda: self.controller.show_frame(RegisterFrame)).grid(row= 8, column= 4, pady= 5)

    #Function to check the login status
    def login(self):

        #import validate login only for this function call
        from data_handler import validate_login

        #Get student id and password from entry box
        studentID = self.studentID.get().strip()
        password = self.password.get().strip()

        #Validate format for studentid and password
        if not v.validate_id(studentID):
            print("Invalid Student ID")
            return 
        
        if not v.validate_password(password):
            print("Invalid Password")
            return
        
        #Run validate login to get the status (admin/student/failed login)
        status = validate_login(studentID.strip(), password.strip())

        #If admin open admin page
        if status == "Admin":
            self.controller.show_frame(AdminFrame)

        #if student open student page
        elif status == "Student":
            self.controller.show_frame(StudentFrame)

        else:
            print("Login Failed")

#Register Frame
class RegisterFrame(BaseFrame):
    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        #Label for title
        tk.Label(self.form, text ="Register", font = LARGEFONT).grid(row= 0, column= 4, padx= 10, pady= 10)

        #Label and entry for name
        tk.Label(self.form, text="Name").grid(row= 2, column= 4)
        self.name = tk.Entry(self.form)
        self.name.grid(row= 3, column= 4)

        #label and entry for age
        tk.Label(self.form, text="Age").grid(row= 5, column= 4)
        self.age = tk.Entry(self.form, validate="key", validatecommand= self.digit_validator())
        self.age.grid(row= 6, column= 4)

        #label and entry for gender
        tk.Label(self.form, text="Gender").grid(row= 7, column= 4)
        self.gender = tk.Entry(self.form)
        self.gender.grid(row= 8, column= 4)

        #label and entry for phone number
        tk.Label(self.form, text="Phone Number").grid(row= 9, column= 4)
        self.phone_number = tk.Entry(self.form, validate="key", validatecommand= self.digit_validator)
        self.phone_number.bind("<KeyRelease>", self.on_phone_change)
        self.phone_number.grid(row= 10, column= 4)

        #label and entry for email
        tk.Label(self.form, text="Email").grid(row= 11, column= 4)
        self.email = tk.Entry(self.form)
        self.email.grid(row= 12, column= 4)

        #label and entry for password
        tk.Label(self.form, text="Password").grid(row= 13, column= 4)
        self.password = tk.Entry(self.form, show= "*")
        self.password.grid(row= 14, column= 4)

        #label and entry for password confirmation
        tk.Label(self.form, text="Confirm Password").grid(row= 15, column= 4)
        self.confirmed = tk.Entry(self.form, show= "*")
        self.confirmed.grid(row= 16, column= 4)

        #Button to register student info
        tk.Button(self.form, text="Register Now", command= lambda: self.register_info()).grid(row= 17, column= 4, pady= 10)

    #function ran when register button is pressed
    def register_info(self):

        #Import functions used only in this function call
        from data_handler import save_student, save_password
        import student
        from security import hash_password

        #Check if the 2 password matches
        if self.confirmed.get().strip() != self.password.get().strip():
            return

        #Check validation for name, email, phone, password
        if not v.validate_name(self.name.get().strip()):
            return 
        
        if not v.validate_email(self.email.get().strip()):
            return
        
        if not v.validate_phone(self.phone_number.get().strip()):
            return
        
        if not v.validate_password(self.password.get().strip()):
            return

        #store the student records
        record = student.StudentRecord(
            studentID= student.StudentRecord.studentID_generator(),
            name= self.name.get().strip(),
            age= self.age.get().strip(),
            gender= self.gender.get().strip(),
            phoneNumber= self.phone_number.get().strip(),
            email= self.email.get().strip(),
        )
        
        #Try to save the studen records and hashed password into the database and goes to student page when succeeds
        try:
            save_student(record)
            save_password(record.studentID, hash_password(self.password.get().strip()))
            print("Account Created")
            self.controller.show_frame(StudentFrame)

        except ValueError as e:
            print(e)        

#!!!! Everything below is work in progress
#I just copied a quick page layout from google
#Remember to subclass with baseframe rather than tk.frame

class AdminFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(self.form, text ="Admin Page", font = LARGEFONT).grid(row = 0, column = 4, padx = 10, pady = 10)
 

class StudentFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(self.form, text ="Student Page", font = LARGEFONT).grid(row = 0, column = 4, padx = 10, pady = 10)
        



#Create gui object
app = AppGui()
app.mainloop()