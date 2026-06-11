# JavaScript Attacks - High

## Step 1

* Opened JavaScript Attacks page.
* Security level set to High.

**Screenshot:** `01_target_page.JPG`

## Step 2

* Submitted the phrase `success`.
* Captured the request in Burp Suite.
* Observed the generated token and request parameters.

**Screenshot:** `02_burp_request.JPG`

## Step 3

* Reviewed and deobfuscated the client-side JavaScript logic.
* Identified the token generation process:

  * Reverse the phrase.
  * Apply SHA-256 with prefix `XX`.
  * Apply SHA-256 again with suffix `ZZ`.
* Generated the correct token.
* Sent the request with:

  ```text
  phrase=success
  token=ec7ef8687050b6fe803867ea696734c67b541dfafb286a0b1239f42ac5b0aa84
  ```
* Server returned **"Well done!"**.

**Screenshot:** `03_successful_bypass.JPG`

## Result

* Successfully bypassed the High-level JavaScript validation.
* Generated a valid token by reverse-engineering the obfuscated client-side code.

## Reason

* Security logic was implemented in client-side JavaScript.
* Although obfuscated, the token generation algorithm could still be analyzed and reproduced.
* Any security mechanism executed on the client can ultimately be reverse-engineered.

## Fix

* Move security-critical validation to the server side.
* Do not rely on JavaScript obfuscation for protection.
* Generate and validate tokens on the server.
* Treat all client-side values as untrusted input.
