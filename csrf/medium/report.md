# CSRF - Medium

## Step 1
Submitted password change form normally.

![Fig 1](images/fig1-success.jpg)

## Step 2
Observed request parameters in URL.

## Step 3
Recreated request manually.

## Step 4
Password change was still successful.

![Fig 2](images/fig2-bypass.jpg)

## Result
Application is still vulnerable to CSRF.

## Reason
No CSRF token implemented, weak validation.

## Fix
- Use CSRF tokens
- Validate request origin
- Use POST method