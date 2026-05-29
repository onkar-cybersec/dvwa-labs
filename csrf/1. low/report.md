# CSRF - Low

## Step 1

Captured the password change request using Burp Suite.

## Step 2

Sent the request to Repeater and modified the password parameters.

## Step 3

Resent the request and observed a successful response.

Result:

```text
Password Changed.
```

## Step 4

Executed a forged CSRF request and observed the request being processed automatically.

## Result

Successfully changed the administrator password through a forged request.

## Reason

No CSRF protection is implemented. The application accepts sensitive requests without validating the request source.

## Fix

* Implement CSRF tokens
* Validate request origin
* Use SameSite cookies

## Screenshots

![Target Page](images/00-target-page.JPG)

![Captured Request](images/01-request.JPG)

![Repeater Request](images/02-repeater-request.JPG)

![CSRF Request Executed](images/03-csrf-poc-executed.JPG)
