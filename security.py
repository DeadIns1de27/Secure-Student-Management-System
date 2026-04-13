"""
Description:
File dedicated to SHA-256 hashing with salting included
Contains:
1) password hashing function
2) password verification function
"""

#Import hashing library, os for salt generation, hmac to compare digest
import hashlib
import os
import hmac

#function hash_password takes string input and returns the hashed string
def hash_password(password: str) -> str:

    #Create random salt
    salt = os.urandom(32)

    #Create a key with sha-256, with salting added
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        10000
    )

    #Return salt with key for storage
    #Ex. salt:key
    return salt.hex() + ":" + key.hex()


#function verify_password takes password stored and compared with input password
def verify_password(stored_password: str, input_password: str) -> bool:

    #split the salt and key
    salt_hex, key_hex = stored_password.split(":")

    #turn salt and key back into bytes
    salt = bytes.fromhex(salt_hex)
    stored_key = bytes.fromhex(key_hex)

    #hash new password into new key for comparison
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        input_password.encode('utf-8'),
        salt,
        10000
    )

    #Use hmac.compare_digest for safe comparison.
    #Returns bool
    return hmac.compare_digest(stored_key, new_key)