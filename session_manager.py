'''
Description:
This file will track the user's login state.
It will count the number of login attempts and increment after each failed attempt.
If the correct email and password are input, return true.
After three failed attempts, return false.
'''

from data_handler import validate_login
from two_factor_authentication import TwoFactorAuthentication

class SessionManager():
    def __init__(self):
        self.session = None
        self.attempts = 0
        self.max_attempts = 3

    def track_login_attempts(self, userID, password):
        #initialize functions to track number of login attempts
        if self.attempts >= self.max_attempts:
            return "Locked"

        status = validate_login(userID, password)
        if status is None:
            if self.attempts >= self.max_attempts:
                return "Locked"
            self.attempts += 1
            return"Incorrect"

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