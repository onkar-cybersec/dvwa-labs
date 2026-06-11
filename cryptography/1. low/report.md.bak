# Cryptography Problems - Low

## Steps

### 1. Access the Vulnerable Page

* Navigated to **DVWA → Cryptography Problems** with security level set to **Low**.
* Observed the intercepted encrypted message.

**Screenshot:** `01_target_page.JPG`

### 2. Decode the Intercepted Message

* Copied the intercepted ciphertext:

```text
Lg4WGlQZChhSFBYSEB8bBQtPGxdNQSwEHREOAQY=
```

* Pasted it into the Message field.
* Selected **Decode** and submitted the request.

The application revealed:

```text
Your new password is: Olifant
```

**Screenshot:** `02_decoded_password.JPG`

### 3. Authenticate with the Recovered Password

* Used the recovered password:

```text
Olifant
```

* Logged into the application successfully.

**Screenshot:** `03_successful_login.JPG`

## Result

The encrypted message was successfully decoded, revealing the user's password. The recovered password allowed successful authentication.

## Reason

The application uses a weak XOR-based encryption scheme with a hardcoded key:

```text
wachtwoord
```

Because the application provides both encryption and decryption functionality, an attacker can decode intercepted messages and recover sensitive information.

## Fix

* Do not use custom XOR encryption for protecting sensitive data.
* Use modern cryptographic algorithms such as AES-GCM.
* Store passwords using secure password hashing functions (bcrypt, Argon2, PBKDF2).
* Never transmit recoverable passwords through encrypted messages.
