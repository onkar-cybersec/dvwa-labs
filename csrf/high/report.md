# CSRF - High

## Step 1
Submitted password change form normally.

![Fig 1](images/fig1-normal.jpg)

## Step 2
Observed CSRF token in request.

## Step 3
Attempted CSRF attack without token.

## Step 4
Request failed.

![Fig 2](images/fig2-failed.jpg)

## Result
CSRF attack was not successful.

## Reason
Application uses CSRF token which is required for valid requests.

## Conclusion
Proper CSRF protection is implemented.

## Fix
- Use CSRF tokens (already implemented)
- Validate session and request origin