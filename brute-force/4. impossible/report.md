# Brute Force - Impossible

## Step 1
Captured the login request from the DVWA Brute Force page using Burp Suite.

![Request Captured](images/01-request.__temp__.JPG)

## Step 2
Sent the request to Burp Intruder and configured an automated brute-force attack.

![Injection Position Identified](images/02-positions.JPG)

## Step 3
Submitted multiple password payloads against the application.

![Payloads Configured](images/03-payloads.__temp__.JPG)

## Step 4
Analyzed the responses and observed that all returned similar results.

![Execution Results](images/04-results.__temp__.JPG)

## Result
The automated brute-force attack was unsuccessful.

## Reason
The application implements strong authentication controls and anti-brute-force protections, preventing attackers from identifying valid credentials through automated testing.

## Fix
The application already implements effective protections:
- Secure session handling.
- Request validation.
- Strong authentication controls.
- Anti-brute-force mechanisms.