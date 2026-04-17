'''
Description:
This file will track the user's login state.
It will count the number of login attempts and increment after each failed attempt.
If the correct email and password are input, return true.
After three failed attempts, return false.
'''
from security import verify_password

class SessionManager():
    def __init__(self):
        self.session = None

    def track_attempts(self, user):
        #initialize functions to track number of login attempts
        login_attempts = 0
        max_attempts = 3

        #loop through as long as the max attempts haven't been reached
        while login_attempts < max_attempts:

            #prompt user for email and password
            input_email = input("Enter email: ")
            input_password = input("Enter password: ")

            #check for valid email and password
            #currently verify_email is not done so it is a placeholder for now
            if verify_email(user.email, input_email) and verify_password(user.password, input_password):
               print("Correct email and password")
               return True
            else:
                print("Incorrect email or password")
                login_attempts += 1

        print("Too many incorrect login attempts")
        return False

#Example / Test Case, only works when executed directly
if __name__ == "__main__":
    manager = SessionManager()
    manager.track_attempts(None)