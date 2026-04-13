# Brute Force - High

## Step 1
Captured login request using Burp Suite.

## Step 2
Attempted brute force attack using Intruder.

## Step 3
Sent multiple password payloads.

## Step 4
Observed that all responses were similar.

## Result
Could not reliably identify correct password using automated brute force.

## Reason
Application hides response differences, making detection difficult.

## Conclusion
Brute force attack becomes ineffective due to lack of clear response indicators.

## Fix
- Rate limiting
- Account lockout
- CAPTCHA
- Monitoring suspicious activity