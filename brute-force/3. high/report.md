# Brute Force - High

## Step 1
Captured the login request from the DVWA Brute Force page using Burp Suite.

![Request Captured](images/01-request.__temp__.JPG)

## Step 2
Sent the request to Burp Intruder and configured the password parameter for testing.

![Injection Position Identified](images/02-positions.__temp__.JPG)

## Step 3
Submitted multiple password payloads using Intruder.

![Payloads Configured](images/03-payloads.__temp__.JPG)

## Step 4
Reviewed the responses and observed that they appeared similar.

![Execution Results](images/04-results.__temp__.JPG)

## Result
Unable to reliably identify the correct password using automated brute-force techniques.

## Reason
The application hides response differences, preventing attackers from easily distinguishing successful and failed login attempts.

## Fix
- Maintain consistent response handling.
- Implement rate limiting.
- Enforce account lockout mechanisms.
- Add CAPTCHA protection.
- Monitor suspicious authentication activity.