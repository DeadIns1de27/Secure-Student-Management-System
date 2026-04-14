"""
Description:
Using regex to validate strings:
1) Names (capitalized initials, no digits)
2) phones (xxx-xxx-xxxx)
3) email extentions (.yahoo, .gmail, .ucmo)
4) password validator (start with !@#$%^&* and be 6-12 characters long)
"""

#Import regex library
import re

#Validate names
def validate_name(name: str) -> bool:

    #(Initials capitalized, no numbers)
    pattern = r'^[A-Z][a-z]*(?: [A-Z][a-z]*)*$'
    return bool(re.fullmatch(pattern, name))

#Validate phone number
def validate_phone(phone: str) -> bool:

    #(xxx-xxx-xxxx)
    pattern = r'^\d{3}-\d{3}-\d{4}$'
    return bool(re.fullmatch(pattern, phone))
    
#Validate emails
def validate_email(email: str) -> bool:

    #only allows yahoo, gmail or ucmo
    pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|ucmo\.edu)$'
    return bool(re.fullmatch(pattern, email))

#Validate password
def validate_password(password: str) -> bool:

    #password must start with !@#$%^&*, and be 6 - 12 characters long
    pattern = r'^[!@#$%^&*][A-Za-z0-9!@#$%^&*]{5,11}$'
    return bool(re.fullmatch(pattern, password))



#Example / Test Case, only works when executed directly
if __name__ == "__main__":
    print(validate_name("Marcus Chow Jian Shen"))
    print(validate_name("Marcus Chow jian shen"))
    print(validate_phone("660-888-8888"))
    print(validate_phone("660-888-88884"))
    print(validate_email("lxm14580@ucmo.edu"))
    print(validate_email("lxm14580@yahoo.com"))
    print(validate_email("lxm14580@gmail.com"))
    print(validate_email("lxm14580@hotmail.com"))
    print(validate_password("!!!!!sdas"))
    print(validate_password("university123"))