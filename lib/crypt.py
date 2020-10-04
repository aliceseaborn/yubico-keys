#!/usr/bin/env python
"""Provides cryptographic processes to secure Python applications.

Includes the ability to generate secure keyfiles, encrypt files
using keyfiles, hash passwords, verify password attempts against a
hash, and verify a Yubico one time password.
"""

from passlib.context import CryptContext
from cryptography.fernet import Fernet
import requests
import random
import string
import os

__author__ = "Alice Seaborn, Austin Dial"

__version__ = "0.0.0"
__maintainer__ = "Alice Seaborn"
__email__ = "adial@mail.bradley.edu"
__status__ = "Prototype"



def generate_keyfile(filename):
    """
    Generates a Fernet key and stores the key in
    the provided .key file with the provided path.
    """
    
    if filename[-4:] == ".key":
        if not os.path.isfile(filename):
            os.mknod(filename)
        
        key = Fernet.generate_key()
        with open(filename, "wb+") as file:
            file.write(key)
            file.close()
    else:
        raise TypeError("The provided file must be a " \
        "key file.")


def load_keyfile(filename):
    """
    Reads the key stored in the provided keyfile and
    returns the key information.
    """
    
    if filename[-4:] == ".key":
        if not os.path.isfile(filename):
            os.mknod(filename)
        
        with open(filename, "rb+") as file:
            key = file.read()
            file.close()
        return key
    else:
        raise TypeError("The provided file must be a " \
        "key file.")


def encrypt_file(source, destination, key):
    """
    Encrypts the provided source file using the
    provided key and saves the encrypted data to
    the destination file.
    """
    
    if not os.path.isfile(source):
        os.mknod(source)
        
    with open(source, "rb+") as file:
        source = file.read()
        file.close()
        
    fernet = Fernet(key)
    encrypted = fernet.encrypt(source)
    
    if not os.path.isfile(destination):
        os.mknod(destination)
    
    with open(destination, "rb+") as file:
        file.write(encrypted)
        file.close()


def decrypt_file(source, destination, key):
    """
    Decrypts the provided source file using the
    provided key and saves the decrypted data to
    the destination file.
    """
    
    if not os.path.isfile(source):
        os.mknod(source)
        
    with open(source, "rb+") as file:
        source = file.read()
        file.close()
        
    fernet = Fernet(key)
    encrypted = fernet.decrypt(source)
    
    if not os.path.isfile(destination):
        os.mknod(destination)
    
    with open(destination, "rb+") as file:
        file.write(encrypted)
        file.close()


def _define_crypt_contect(rounds):
    return CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=rounds
    )


def encrypt_password(password):
    """
    Encrypts the plaintext password provided.
    """
    
    crypt_context = _define_crypt_contect(30000)
    
    return crypt_context.hash(password)


def verify_password(password, hashed):
    """
    Verifies if the provided password matches
    the hash for the given account.
    """
    
    crypt_context = _define_crypt_contect(30000)
    
    return crypt_context.verify(password, hashed)


def _rand_string(length):
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits)
                    for _ in range(25))


def validate_otp(client_id, otp):
    """
    Validates the provided OTP against the
    Yubico API for the provided client id.
    """
    
    nonce = _rand_string(25)

    url = f"https://api.yubico.com/wsapi/2.0/verify?"\
        f"id={client_id}&otp={otp}&nonce={nonce}"

    raw_response = requests.get(url).text.splitlines()

    keys = list(); values = list()
    for field in raw_response:
        if len(field):
            keys.append(field.split("=", 1)[0])
            values.append(field.split("=", 1)[1])

    response = dict(zip(keys, values))
    
    return response



if __name__ == '__main__':
    print("Crypt module cannot be run as an executable.")
