# Cryptography Problems - Comparison Report

## Low

### Weakness

* Repeating XOR encryption with a hardcoded key.
* Application provides both encryption and decryption functionality.

### Impact

* Intercepted messages can be decoded.
* Sensitive information such as passwords can be recovered.

### Result

Vulnerable

---

## Medium

### Weakness

* Uses AES-128-ECB.
* ECB encrypts blocks independently and provides no integrity protection.

### Impact

* Ciphertext blocks can be rearranged.
* Session tokens can be forged.
* Privilege escalation to administrator is possible.

### Result

Vulnerable

---

## High

### Weakness

* Uses AES-128-CBC with a client-controlled IV.
* No integrity protection is applied.

### Impact

* CBC bit-flipping attack allows modification of decrypted plaintext.
* User ID can be changed from a standard user to an administrator.

### Result

Vulnerable

---

## Impossible

### Protection

* Uses AES-256-GCM.
* Includes authenticated encryption and integrity verification.
* Random IV generated for each token.

### Impact

* Token tampering is detected.
* Bit-flipping and token forgery attacks fail.

### Result

Not Vulnerable

---

## Conclusion

The security of the implementation improves progressively across the levels:

* **Low** fails due to weak custom cryptography.
* **Medium** fails due to insecure ECB mode.
* **High** fails because CBC encryption lacks integrity protection.
* **Impossible** correctly implements authenticated encryption using AES-256-GCM, preventing token manipulation and privilege escalation.
