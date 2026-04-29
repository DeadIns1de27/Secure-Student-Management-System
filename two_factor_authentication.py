'''
Description:
File dedicated to two-factor authentication via Google Authenticator using
the pyotp library

pyotp uses Google Authenticator and a time-based code. Every thirty seconds, a new six-digit
code is generated, which can be found in the Authenticator app. The user must enter this code
to complete their two-factor authentication process.

def generate_user_key generates a random
32 character long base32 upi key that is special for each user.

def display_qr_code takes the individualized secret_key from the
student (based off of their studentID), creates a
scannable QRCode file, and returns the filename

def verify_key gives the user three attempts to input the correct six-digit
code from their Google Authenticator app. If they enter the correct code, return true.
If they fail three times, return false
'''

#import pyotp and qrcode
import pyotp
import qrcode
import io
from PIL import Image, ImageTk

#TwoFactorAuthentication() Class
class TwoFactorAuthentication():
    #Initializer method
    def __init__(self):
        #Issuer name will be displayed in the Google Authenticator app
        #Set issuer name to company/program name
        self.issuer_name = "Secure Student Management System"

    def generate_user_key(self):
        #generate random 32 character base32 code
        secret_key = pyotp.random_base32()
        #return the key
        return secret_key

    def display_qr_code(self, secret_key, studentID):
        #create uri code
        uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name = str(studentID),
                                                    issuer_name = self.issuer_name)
        #convert uri to a file based off studentID 700######
        qr = qrcode.make(uri)

        qr = qr.resize((200, 200))
        photo = ImageTk.PhotoImage(qr)

        return photo

    def verify_key(self, secret_key, code):
        #initializes one time password based on current time and secret key
        totp = pyotp.TOTP(secret_key)
 
        return totp.verify(code)

#Example / Test Case, only works when executed directly
if __name__ == "__main__":
    tfa = TwoFactorAuthentication()
    print("Must complete 2FA")
    key = tfa.generate_user_key()
    print(f"The QRCode filename is {tfa.display_qr_code(key, '700783695')}")
    tfa.verify_key(key)
