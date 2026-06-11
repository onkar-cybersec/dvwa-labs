# DVWA Insecure CAPTCHA - Low Level

## Step 1
Opened the Insecure CAPTCHA page with security level set to Low.

![Target Page](images/01-target-page.__temp__.JPG)

## Step 2
Completed the CAPTCHA and reached the confirmation stage.

![CAPTCHA Passed](images/02-captcha-passed.__temp__.JPG)

## Step 3
Intercepted the final request and confirmed it only used `step=2`.

![Step 2 Request](images/03-step2-request.__temp__.JPG)

## Result
The password was changed successfully.

![Password Changed](images/04-password-changed.__temp__.JPG)

## Reason
The CAPTCHA is checked only in step 1.  
The real password change happens in step 2 without CAPTCHA verification.

## Fix
Validate CAPTCHA on the final password change request and enforce server-side workflow checks.