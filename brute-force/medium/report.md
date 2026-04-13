# Brute Force - Medium

## Step 1
Captured login request using Burp Suite at Medium security level.

## Step 2
Sent request to Intruder and targeted password parameter.

## Step 3
Used common password list.

## Step 4
Observed response differences to identify correct password.

## Result
Brute force attack was still successful.

## Reason
Protection mechanisms were weak and could be bypassed.

## Fix
- Implement strong rate limiting
- Account lockout
- CAPTCHA
- Logging and monitoring

## Screenshots

![Request](images/request.jpg)
![Positions](images/positions.jpg)
![Payloads](images/payloads.jpg)
![Results](images/results.jpg)