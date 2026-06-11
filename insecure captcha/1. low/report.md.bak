# DVWA Insecure CAPTCHA - Low Level

## Step 1
Opened the Insecure CAPTCHA page with security level set to Low.

![Target Page](screenshots/01-target-page.jpg)

## Step 2
Completed the CAPTCHA and reached the confirmation stage.

![CAPTCHA Passed](screenshots/02-captcha-passed.jpg)

## Step 3
Intercepted the final request and confirmed it only used `step=2`.

![Step 2 Request](screenshots/03-step2-request.JPG)

## Result
The password was changed successfully.

![Password Changed](screenshots/04-password-changed.jpg)

## Reason
The CAPTCHA is checked only in step 1.  
The real password change happens in step 2 without CAPTCHA verification.

## Fix
Validate CAPTCHA on the final password change request and enforce server-side workflow checks.