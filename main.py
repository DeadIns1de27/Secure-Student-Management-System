'''
Description:
File used to initiate program
'''

#Import the gui
from gui import AppGui

#Create main function
def main():

    #Initialise gui and run it
    app = AppGui()
    app.mainloop()

#Only run when this file is executed directly
if __name__ == "__main__":
    main()