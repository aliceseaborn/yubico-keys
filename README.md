# Yubico Keys

Development of cryptographic tools for securely encrypting files, checking passwords against hashes and validating Yubico OTPs from the Yubikey 5 NFC.

This repository contains:

1. The repository requirements in `requirements.txt`
2. The Jupyter Notebook development documentation in `project/Yubico-Keys.ipynb`
3. A static HTML webpage of the documentation in `project/Yubico-Keys.html`
4. A module containing all cryptographic code in `project/lib/crypt.py`
5. A key generated from the code in `project/keys/*`
6. Figures used by the notebook and webpage in `project/jupyter-figures/*`



## Table of Contents

- [Background](#background)
- [Usage](#usage)
    - [Encrypt File](#encrypt-file)
    - [Decrypt Encrypted File](#decrypt-encrypted-file)
    - [Generate Hash](#generate-hash)
    - [Verify Password](#verify-password)
    - [Validate Yubico OTP](#validate-yubico-otp)



## Background

[Yubico](http://www.yubico.com) manufactures low-cost security key fobs for multi/two-factor authentication (2FA), One-Time Passwords (OTP) and Univeral Second Factor (U2F). By requiring a physical device with a key that quickly expires in order to authenticate the user, cyber attacks become more difficult to pull off. Using the Yubikey 5 NFC, python processes and applications can be secured. In addition to the Yubico API, authentication methods are provided for encrypting files and checking passwords against a generated hash. These methods allow for additional layers of security to be added to future Python projects and APIs.



## Usage

Install the requirements in a python environment using the included requirements file. Then navigate to the `project` directory.

```sh
pip install -r requirements.txt
```

Import the `crypt` module from `lib`.

```python
>>> from lib.crypt import *
```

### Encrypt File

In order to encrypt a file, first generate a keyfile and save it to a local directory. Then read the key to a local variable. Finally, encrypt the file by providing a source directory to the plaintext file, a destination directory to the new encrypted file and the key you created.

```python
>>> generate_keyfile("keys/key.key");
>>> key = load_keyfile("keys/key.key")
>>> encrypt_file("file.txt", "secured-file.txt", key);
```

### Decrypt Encrypted File

Load the key that was used to encrypt the file. Decrypt the file by providing the source path to the encrypted file, the destination path to the plain-text and the key that you loaded.

```python
>>> key = load_keyfile("keys/key.key")
>>> decrypt_file("secured-file.txt", "plaintext-file.txt", key);
```

### Generate Hash

In order to hash a password, simply pass in the plaintext password and capture the output as the hash.

```python
>>> hashed = encrypt_password("password")
```

### Verify Password

To verify a user's login attempt by passing the user's input along with the hashed password corresponding to their account.

```python
>>> hashed = encrypt_password("password")
>>> verify_password("Passw0rd", hashed)
False
>>> verify_password("password", hashed)
True
```

### Validate Yubico OTP

The Yubico API requires the accountholders `client_id` and the OTP being validated. Pass both to `validate_otp()`.

```python
>>> validate_otp("012345", "...")
{'h': '...',
 't': '2020-10-04T03:57:44Z0974',
 'otp': '...',
 'nonce': '...',
 'sl': '100',
 'status': 'OK'}
```
