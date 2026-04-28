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
import student as s
import data_handler as dh

#Font and size for titles
LARGEFONT =("Times New Roman", 35)

#Main app class: controls each frame displayed
class AppGui(tk.Tk):

    #Initialize the gui
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.title("Secure Student Management System")  #App window title

        self.geometry("800x600")    #App window size

        self.current_user = None

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
 
        self.show_frame(LoginFrame)     #Default frame is login
 
    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]

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
        
    #Event handler that
    def on_phone_change(self, event):

        value = self.phone_number.get()

        formatted = self.format_phone(value)

        self.phone_number.delete(0, "end")
        self.phone_number.insert(0, formatted)

    def get_current_student(self):
        from data_handler import load_student
        return load_student(self.controller.current_user)


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
        self.controller.current_user = studentID

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
            email= self.email.get().strip()
        )
        
        #Try to save the studen records and hashed password into the database and goes to student page when succeeds
        try:
            save_student(record)
            save_password(record.studentID, hash_password(self.password.get().strip()))
            print("Account Created")
            self.controller.show_frame(LoginFrame)

        except ValueError as e:
            print(e)        

#Admin Page
class AdminFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(self.form, text ="Admin Page", font = LARGEFONT).grid(row = 0, column = 0, pady = 10)

        tk.Label(self.form, text = "Enter Student ID").grid(row = 1, column = 0, padx = 10)

        self.entry = tk.Entry(self.form)
        self.entry.grid(row = 2, column = 0)

        tk.Button(self.form, text = "Submit", command = self.displayStudent).grid(row = 2, column = 1, sticky = "w")

        self.editButton = tk.Button(self.form, text = "Edit", command = self.editStudent)
        self.editButton.grid(row = 7, column = 1, pady = 10)
        self.editButton.grid_remove()

        self.deleteButton = tk.Button(self.form, text = "Delete", command = self.deleteStudent)
        self.deleteButton.grid(row = 3, column = 1, sticky = "w")
        self.deleteButton.grid_remove()

        #Button to log out
        tk.Button(self.form, text="Log Out", command= lambda: self.controller.show_frame(LoginFrame)).grid(row = 6, column = 0, padx = 10, pady = 10)
        
        self.data_frame = tk.Frame(self.form, bd = 2, relief = "groove", padx = 10, pady = 10)
        self.data_frame.grid(row = 4, column = 0, columnspan = 2, pady = 10)
        

    def displayStudent(self):

        #Gets student data from database
        enteredID = self.entry.get()
        student = dh.load_student(enteredID)

        #Clears old data
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        #Displays student data
        row = 0
        for key, value in student.items():
            tk.Label(self.data_frame, text = f"{key}").grid(row = row, column = 0, sticky = "w", padx = 5, pady = 2)
            tk.Label(self.data_frame, text = str(value)).grid(row = row, column = 1, sticky = "w", padx = 5, pady = 2)
            row += 1

        self.currentData = student

        self.editButton.grid()
        self.deleteButton.grid()

    def editStudent(self):

        #Clear frame
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        self.edit_entries = {}

        row = 0
        for key, value in self.currentData.items():
            tk.Label(self.data_frame, text = f"{key}").grid(row = row, column = 0, sticky = "w")

            entry = tk.Entry(self.data_frame)
            entry.insert(0, str(value))
            entry.grid(row = row, column = 1, sticky = "w")

            self.edit_entries[key] = entry
            row += 1

        self.editButton.config(text = "Save", command = self.saveStudent)

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

        self.editButton.config(text = "Edit", command = self.edit_entries)

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
        tk.Label(self.form, text ="Student Page", font = LARGEFONT).grid(row = 0, column = 4, columnspan=2, padx = 10, pady = 10)        
        tk.Button(self.form, text= "Log Out", command=lambda: self.controller.show_frame(LoginFrame)).grid(row= 20, column= 4, columnspan=2, padx= 10, pady= 10)

    #Function that loads user ID from login

    def load_data(self):
    #Get the student record
        self.record = self.get_current_student() 
        row = 1

        #Loop through all the records and display the label and the key
        for label, key in self.record.items():
            
            if label == "adminStatus":
                continue

            tk.Label(self.form, text=f"{label}:", width=20, anchor="w").grid(row=row, column=4, sticky="w", padx= 5, pady= 5)

            tk.Label(self.form, text= key).grid(row=row, column=5, sticky="w", padx= 5, pady= 5)

            row += 1



#Create gui object
app = AppGui()
app.mainloop()