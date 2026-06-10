# Cryptography Problems - Impossible

## Steps

### 1. Access the Vulnerable Page

* Navigated to **DVWA → Cryptography Problems** with security level set to **Impossible**.
* Obtained a valid encrypted token and IV.

**Screenshot:** `01_target_page.JPG`

### 2. Attempt Token Tampering

* Intercepted the token validation request using Burp Suite.
* Sent the request to Burp Repeater.
* Modified a single character in the IV value while keeping the token unchanged.
* Resubmitted the altered request.

**Screenshot:** `02_token_tampering_blocked.JPG`

## Result

The application rejected the modified token and returned:

```text
Unable to decrypt token
```

No privilege escalation or token manipulation was possible.

## Reason

The application uses:

```text
AES-256-GCM
```

AES-GCM provides:

* Confidentiality (encryption)
* Integrity protection (authentication tag)

Any modification to:

* Ciphertext
* IV (nonce)
* Authentication tag

causes verification to fail before the plaintext is accepted.

Unlike the High level CBC implementation, attackers cannot perform bit-flipping attacks because the authentication tag detects tampering.

## Fix

* Continue using authenticated encryption such as AES-GCM.
* Generate a random IV for each token.
* Verify authentication tags before processing decrypted data.
* Reject tokens that fail integrity validation.
