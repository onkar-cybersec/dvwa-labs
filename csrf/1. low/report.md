# CSRF - Low

## Step 1
Captured the password change request using Burp Suite.

![Target Page](images/00-target-page.JPG)

## Step 2
Sent the request to Repeater and modified the password parameters.

![Captured Request](images/01-request.JPG)

## Step 3
Resent the modified request and observed a successful password change response.

![Repeater Request](images/02-repeater-request.JPG)

## Step 4
Executed a forged CSRF request and observed that it was processed automatically by the application.

![CSRF Request Executed](images/03-csrf-poc-executed.JPG)

## Result
Successfully changed the administrator password through a forged request.

## Reason
The application does not implement CSRF protection and accepts sensitive requests without verifying their origin.

## Fix
- Implement Anti-CSRF tokens.
- Validate request origin.
- Use SameSite cookie attributes.
- Require re-authentication for sensitive actions.