# DVWA Insecure CAPTCHA - Medium Level

## Step 1
Opened the Insecure CAPTCHA page with security level set to Medium.

![Target Page](screenshots/01-target-page.jpg)

## Step 2
Completed the CAPTCHA and reached the confirmation stage.

![CAPTCHA Passed](screenshots/02-captcha-passed.jpg)

## Step 3
Intercepted the final request and observed the hidden parameter `passed_captcha=true`.

![Intercepted Request](screenshots/03-intercepted-request.jpg)

## Result
Modified the hidden parameter and forwarded the request. The password was changed successfully.

![Password Changed](screenshots/04-password-changed.jpg)

## Reason
The application trusts the client-side hidden parameter `passed_captcha`.  
An attacker can modify this value and bypass the CAPTCHA protection.

## Fix
Store CAPTCHA validation status on the server side and verify it during the final password change request.