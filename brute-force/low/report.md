
# Brute Force - Low

## Step 1
Captured login request using Burp Suite.

## Step 2
Sent request to Intruder and selected password parameter.

## Step 3
Used common password list:
admin, password, 123456, etc.

## Step 4
Observed response length difference.
Password "password" had different length (4986).

## Result
Successfully identified valid credentials:
username: admin
password: password

## Reason
No brute force protection implemented.

## Fix
- Add rate limiting
- Account lockout
- CAPTCHA

## Screenshots

![Request Captured](images/01-request.JPG)
![Injection Point Identified](images/02-positions.JPG)
![Payloads Added](images/03-payloads.JPG)
![Execution Results](images/04-results.JPG)
