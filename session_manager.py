'''
Description:
This file will track the user's login state.
It will count the number of login attempts and increment after each failed attempt.
If the correct email and password are input, return true.
After three failed attempts, return false.
'''

from data_handler import validate_login

class SessionManager():
    def __init__(self):
        self.session = None
        self.attempts = 0
        self.max_attempts = 3

    def track_login_attempts(self, userID, password):
        #if attempts are 3+, lock the user out
        if self.attempts >= self.max_attempts:
            return "Locked"

        #attempt to login the user with their id and password
        status = validate_login(userID, password)

        #increment login attempts
        self.attempts += 1

        #if login does not work (incorrect ID or Password), return incorrect
        #unless it was their final attempt, then return locked
        if status is None:
            if self.attempts >= self.max_attempts:
                return "Locked"
            return"Incorrect"

        #reinitialize login attempts to 0 and return admin/student status
        elif status == "Admin":
            self.attempts = 0
            return "Admin"

        elif status == "Student":
            self.attempts = 0
            return"Student"

#Example / Test Case, only works when executed directly
if __name__ == "__main__":
    manager = SessionManager()
    print(manager.track_login_attempts("700783695", "testPassword"))